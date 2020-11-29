from datetime import timedelta
from typing import Dict, List

import srt


from utils.list_diff import get_list_diff, ListDiffType


def get_only_letters(s):
    """
    删除 s 两边的标点符号，空字符
    """
    len_s = len(s)
    i , j = 0, len_s-1

    while i < len_s and not s[i].isalnum():
        i += 1
    while j >= i and not s[j].isalnum():
        j -= 1

    return s[i:j+1]


def fix_sentence(final_sentence: str, slice_sentence: str) -> str:
    """
    TODO:
    """
    sentence_diff = get_list_diff(
        [get_only_letters(word) for word in final_sentence.split()],
        slice_sentence.split()
    )

    final_sentence_list = final_sentence.split()
    count1 = 0  # 对多于一次的操作进行修正，此时 list 已经变动了
    for s_diff in sentence_diff:
        diff_type, diff_start, diff_count = s_diff
        if diff_type == ListDiffType.EXPAND:
            start = diff_start - count1
            end = diff_start - count1 + 1
            first = '{' + final_sentence_list[diff_start - count1]
            last = '-}'
            middle = ['-' for i in range(diff_count - 2)]
            tmp = [first]
            tmp.extend(middle)
            tmp.append(last)
            final_sentence_list[start: end] = tmp
            count1 -= (diff_count - 1)
        else:
            start = diff_start - count1
            end = diff_start + diff_count - count1
            final_sentence_list[start: end] = ['{' + ','.join(final_sentence_list[start: end]) + '}']
            count1 += (diff_count - 1)

    res = ' '.join(final_sentence_list)
    return res


def detail2srts(detail: Dict, split_number: int=5) -> List[srt.Subtitle]:
    """
    拆分成多个 split_number 个词组成的字幕

    detail: 腾讯云语音识别结果中 ResultDetail 列表的一条数据。
    比如：
    {
        "FinalSentence": "EB. ",
        "SliceSentence": "EB",
        "StartMs": 0,
        "EndMs": 2860,
        "WordsNum": 1,
        "Words": [
            {
                "Word": "EB",
                "OffsetStartMs": 810,
                "OffsetEndMs": 2640
            }
        ],
        "SpeechSpeed": 1.0
    }
    """
    final_sentence = detail['FinalSentence']
    slice_sentence = detail['SliceSentence']
    words = detail['Words']

    if not final_sentence:
        return []

    # fix sentence
    final_sentence = fix_sentence(final_sentence, slice_sentence)

    start_ms = detail['StartMs']
    end_ms = detail['EndMs']

    srts = []
    i = 0

    while i < len(words):
        split_sentence = ' '.join(final_sentence.split()[i: i+split_number])
        offsets = []
        split_start_ms = start_ms + words[i]['OffsetStartMs']
        split_offset_start_ms = words[i]['OffsetStartMs']
        if i + split_number - 1 >= len(final_sentence.split()):
            # 如果不够 split_number 个词，使用整句结尾时间
            split_end_ms = end_ms
        else:
            split_end_ms = start_ms + words[i+split_number-1]['OffsetEndMs']
        # print(split_sentence)
        for word in words[i: i+split_number]:
            offsets.append('{},{}'.format(
                word['OffsetStartMs'] - split_offset_start_ms,
                word['OffsetEndMs'] - split_offset_start_ms
            ))
        offsets_string = ' '.join(offsets)
        content = '\n'.join([offsets_string, split_sentence])

        srts.append(srt.Subtitle(
            index=0,
            start=timedelta(milliseconds=split_start_ms),
            end=timedelta(milliseconds=split_end_ms),
            content=content
        ))
        i += split_number

    return srts
