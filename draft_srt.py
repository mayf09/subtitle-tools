import re

from collections import namedtuple
from datetime import timedelta
from typing import List

import srt


Srt = srt.Subtitle

TIME_OFFSET_INDEX=0
EN_INDEX=1
ZH_INDEX=2

PART_SRT_SEP_REGEX=re.compile(r'(?<=\S)\|\s?|\s?\|(?!\S)')


TimeOffset = namedtuple('TimeOffset', ['start', 'end'])


class DraftSrt(Srt):

    @property
    def time_offset(self) -> List[str]:
        time_offset_string_list = self.get_content_lines()[TIME_OFFSET_INDEX].split(' ')
        return [self.to_time_offset(item) for item in time_offset_string_list]

    @staticmethod
    def to_time_offset(time_offset_string: str) -> TimeOffset:
        tmp = [int(_) for _ in time_offset_string.split(',')]
        return TimeOffset(*tmp)

    @property
    def en_text(self) -> str:
        if not self.has_en_text():
            return None
        return self.get_content_lines()[EN_INDEX]

    @en_text.setter
    def en_text(self, text: str):
        content_lines = self.get_content_lines()
        content_lines[EN_INDEX] = text
        self.content = '\n'.join(content_lines)

    @property
    def zh_text(self) -> str:
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
        part_srt_en_texts = PART_SRT_SEP_REGEX.split(self.en_text)
        part_srt_zh_texts = PART_SRT_SEP_REGEX.split(self.zh_text)
        res = []
        part_srt_start_index = 0
        for i in range(len(part_srt_en_texts)):
            item = part_srt_en_texts[i]
            length = len(item.split())
            if item != '':
                res.append(
                    Srt(index=0,
                        start=self.time_offset_to_timedelta(self.time_offset[part_srt_start_index].start),
                        end=self.time_offset_to_timedelta(self.time_offset[part_srt_start_index+length-1].end),
                        content='\n'.join([part_srt_en_texts[i], part_srt_zh_texts[i]]))
                )
                part_srt_start_index += length
            else:
                res.append(None)
        return res
