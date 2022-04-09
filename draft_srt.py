import re

from collections import namedtuple
from datetime import timedelta
from typing import List, Generator

import srt


Srt = srt.Subtitle

TIME_OFFSET_INDEX=0
EN_INDEX=1
ZH_INDEX=2

PART_SRT_SEP_REGEX=re.compile(r'\s?(?<!\\)\|\s?')
COMMA_REGEX = re.compile(r'\s?(?<!\\),\s?')  # 匹配 , ，不包含 '\,'
FIX_EN_SRT_REGEX = re.compile(r'(?<!\\)\{(.*?)(?<!\\)\}')  # 匹配大括号内的内容，不包含 '\{' '\}'
FIX_SPACE_REGEX = re.compile(r'( +)(?=[ ])|( +)(?=[,.!?] )|( +)(?=[,.!?]\Z)')  # 匹配多个空格或者断句标点之前的空格
FIX_COMMA_REGEX = re.compile(r'\\,')  # 匹配 '\,'
TIME_OFFSET_REGEX = re.compile(r'^\d+,\d+$')


TimeOffset = namedtuple('TimeOffset', ['start', 'end'])


class DraftSrt(Srt):

    @classmethod
    def from_srt(cls, srt):
        obj = cls(srt.index, srt.start, srt.end, srt.content, proprietary=srt.proprietary)
        if not obj.check_time_offset():
            raise ValueError(obj.to_srt())
        if not obj.check_zh_text():
            raise ValueError(obj.to_srt())
        return obj

    @property
    def time_offset(self) -> List[str]:
        time_offset_string_list = self.get_content_lines()[TIME_OFFSET_INDEX].split(' ')
        return [self.to_time_offset(item) for item in time_offset_string_list]

    @staticmethod
    def to_time_offset(time_offset_string: str) -> TimeOffset:
        if not TIME_OFFSET_REGEX.match(time_offset_string):
            raise TimeOffsetParseException('TimeOffset parse error,  string is {}'.format((time_offset_string)))
        tmp = [int(_) for _ in time_offset_string.split(',')]
        return TimeOffset(*tmp)

    @property
    def en_text(self) -> str or None:
        if not self.has_en_text():
            return None
        return self.get_content_lines()[EN_INDEX]

    @en_text.setter
    def en_text(self, text: str):
        content_lines = self.get_content_lines()
        content_lines[EN_INDEX] = text
        self.content = '\n'.join(content_lines)

    @property
    def zh_text(self) -> str or None:
        if not self.has_zh_text():
            return None
        return self.get_content_lines()[ZH_INDEX]

    @zh_text.setter
    def zh_text(self, text: str):
        content_lines = self.get_content_lines()
        content_lines[ZH_INDEX] = text
        self.content = '\n'.join(content_lines)

    def get_content_lines(self) -> List[str]:
        return self.content.split('\n')

    def has_en_text(self) -> bool:
        return len(self.get_content_lines()) >= EN_INDEX + 1

    def has_zh_text(self) -> bool:
        return len(self.get_content_lines()) == ZH_INDEX + 1

    def check_time_offset(self) -> bool:
        if not self.has_en_text():
            return True
        return len(self.time_offset) == len(self.en_text.split())

    def check_zh_text(self) -> bool:

        # 不包含英文字幕
        if not self.has_en_text():
            return True

        # 包含英文字幕，不包含中文字幕
        if not self.has_zh_text():
            return True

        # 既包含英文字幕，又包含中文字幕
        return len(PART_SRT_SEP_REGEX.split(self.en_text)) == len(PART_SRT_SEP_REGEX.split(self.zh_text))

    def time_offset_to_timedelta(self, t):
        return self.start + timedelta(milliseconds=t)

    def get_part_srts(self) -> List[Srt or None]:
        """
        abc d| efg|

        abc d
        efg
        None
        """
        if not self.has_en_text():
            return []
        part_srt_en_texts = PART_SRT_SEP_REGEX.split(self.en_text)
        zh_text = self.zh_text
        if zh_text is None:
            zh_text = ''
        part_srt_zh_texts = PART_SRT_SEP_REGEX.split(zh_text)
        res = []
        part_srt_start_index = 0
        for i in range(len(part_srt_en_texts)):
            item = part_srt_en_texts[i]
            length = len(item.split())
            if item != '':
                if self.has_zh_text():
                    content = '\n'.join([part_srt_en_texts[i], part_srt_zh_texts[i]])
                else:
                    content = '\n'.join([part_srt_en_texts[i]])
                res.append(
                    Srt(index=0,
                        start=self.time_offset_to_timedelta(self.time_offset[part_srt_start_index].start),
                        end=self.time_offset_to_timedelta(self.time_offset[part_srt_start_index+length-1].end),
                        content=content)
                )
                part_srt_start_index += length
            else:
                res.append(None)
        return res

    @staticmethod
    def to_final_srts(draft_srts: List['DraftSrt'], langs: List[str] = ['en', 'zh']) -> Generator[Srt, None, None]:

        tmp = []

        for draft_srt in draft_srts:
            part_srts = draft_srt.get_part_srts()
            length = len(part_srts)
            for i in range(length):
                tmp.append(part_srts[i])
                if i != length - 1:
                    yield __class__.merge_part_srts(tmp, langs)
                    tmp = []

        yield __class__.merge_part_srts(tmp, langs)

    @staticmethod
    def merge_part_srts(part_srts: List[Srt], langs: List[str]=['en', 'zh']) -> Srt:
        part_srts = [_ for _ in part_srts if _ is not None]  # 非空
        if not part_srts:
            raise ValueError('some final srt is blank')
        length = len(part_srts)
        start = part_srts[0].start
        end = part_srts[length - 1].end
        if 'en' in langs:
            en_text = ' '.join([_.content.split('\n')[0] for _ in part_srts])
            en_text = __class__.fix_en_text(en_text)
        if 'zh' in langs:
            zh_text = ''.join([_.content.split('\n')[1] for _ in part_srts if len(_.content.split('\n')) > 1])

        l = locals()
        text = '\n'.join([
            l['{}_text'.format(lang)]
            for lang in langs
        ])

        return Srt(
            index=0,
            start=start,
            end=end,
            content=text
        )

    @staticmethod
    def fix_en_text(text: str) -> str:
        """
        处理英文字幕中的 {word1,word2} {word - - -} {}
        """

        def f(m):
            tmp = m.group(1)
            # '{}'                -> ''
            # '{word1,word2}'     -> 'word1 word2'
            # '{word - -}'        -> 'word'
            # '{ - -}'            -> ''
            # '{word1,word2 - -}' -> 'word1 word2'
            # '{word1\,word2 - -}' -> 'word1,word2'
            # '{word1\,,word2 - -}' -> 'word1, word2'
            res = ' '.join(
                re.split(
                    COMMA_REGEX,
                    re.split(' ', tmp)[0]
                )
            )
            return res

        text1 = FIX_EN_SRT_REGEX.sub(f, text)  # 处理大括号内容
        text2 = FIX_SPACE_REGEX.sub('', text1).strip()  # 处理不合适的空格
        text3 = FIX_COMMA_REGEX.sub(',', text2)

        return text3


class TimeOffsetParseException(Exception):
    pass
