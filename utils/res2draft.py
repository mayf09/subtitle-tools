from datetime import timedelta
from typing import Dict, List

import srt


from utils.get_valid_string import get_valid_string
from utils.list_diff import get_list_diff



def fix_sentence(final_sentence: str, slice_sentence: str) -> str:
    """
    TODO:
    """
    sentence_diff = get_list_diff(
        [get_valid_string(word) for word in final_sentence.split()],
        [get_valid_string(word) for word in slice_sentence.split()]
    )

    final_sentence_list = final_sentence.split()
    diff_count = 0  # 对多于一次的操作进行修正，此时 list 已经变动了
    for s_diff in sentence_diff:
        diff_start1, diff_end1, diff_start2, diff_end2 = s_diff
        start = diff_start1 - diff_count
        end = diff_end1 - diff_count
        first = '{' + ','.join(final_sentence_list[start:end])
        middle = ['-' for i in range(diff_end2 - diff_start2 - 1)]
        last = '}'
        tmp = [first]
        tmp.extend(middle)
        tmp[-1] = tmp[-1] + last
        final_sentence_list[start: end] = tmp
        diff_count += 1
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
