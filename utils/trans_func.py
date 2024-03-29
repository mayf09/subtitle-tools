from collections import namedtuple
from time import sleep
from typing import List


from draft_srt import DraftSrt


PartTextInfo = namedtuple('PartTextInfo', ['index', 'index_i', 'is_blank'])


class RealText:
    """
    part_text_infos: 按 | 拆分的部分文本信息列表
    """

    def __init__(self, content, part_text_infos) -> None:
        self.content = content
        self.part_text_infos = part_text_infos

    def __str__(self) -> str:
        return self.content + \
            '\n' + \
            ','.join(['({} {} {})'.format(*info) for info in self.part_text_infos]) + \
            '\n'


def get_string_list_length(l):
    res = sum([len(_) for _ in l])
    return res


def get_next_index(subs):
    line_index = 0
    inline_index = 0
    for sub in subs:
        count = sub.split('|')
        for i in range(len(count)):
            inline_index = i
            yield(line_index, inline_index)
        line_index += 1


def get_next_real_sub(subs: List[DraftSrt]) -> RealText:
    """
    获取真正字幕（生成器）
    """

    tmp = ''
    pre_part_info = None
    line_index = 0
    inline_index = 0
    part_infos = []
    for sub in subs:
        if len(sub.content.split('\n')) >= 2:
            en_text = sub.content.split('\n')[1]
        else:
            en_text = ''
        if pre_part_info:
            part_infos.append(pre_part_info)
        if tmp == '':
            tmp = en_text
        else:
            tmp = tmp + ' ' + en_text
        parts = tmp.split('|')
        inline_index = 0
        for part in parts[:-1]:
            part_infos.append(PartTextInfo(line_index, inline_index, part.strip() == ''))
            yield RealText(part.strip(), part_infos)
            part_infos = []
            inline_index += 1
        tmp = parts[len(parts)-1]
        pre_part_info = PartTextInfo(line_index, inline_index, tmp.strip() == '')
        line_index += 1
    # 最后一条
    part_infos.append(pre_part_info)
    yield RealText(tmp.strip(), part_infos)


def get_sub_group(subs, limit: int=None):
    res = []

    if limit is None:
        raise ValueError

    real_sub_gen = get_next_real_sub(subs)
    for sub in real_sub_gen:
        # print(sub)

        if len(sub.content) > limit:
            raise Exception('single sub is too long')

        if get_string_list_length([_.content for _ in res]) + len(sub.content) > limit:
            yield(res)
            res = []
            res.append(sub)
        else:
            res.append(sub)

    yield(res)


def trans_group(subs, sub_group, trans_f):
    """
    使用 trans_f 批量修改字幕，并放回原字幕 subs 位置
    """

    first = True
    trans_res = trans_f(
        [DraftSrt.fix_en_text(_.content.split('\n')[0]) for _ in sub_group]
    )
    tmp_parts = []  # 当前 trans_group 在某一行的临时部分
    line_index = 0  # 临时行 index ，是否转换
    trans_index = 0 # trans_res 的 index
    for real_text in sub_group:
        if first:
            first = False
            line_index = real_text.part_text_infos[0].index
        flag = False
        for info in real_text.part_text_infos:
            if line_index == info.index:
                if not info.is_blank and not flag:
                    flag = True
                    tmp_parts.append(trans_res[trans_index])
                    trans_index += 1
                else:
                    tmp_parts.append('')
            else:
                # 如果草稿字幕换行，写入上一行
                if len(subs[line_index].content.split('\n')) < 3:
                    # 是否已经有第 3 行
                    if len(tmp_parts) == 1 and tmp_parts[0] == '' and len(subs[line_index].content.split('|')) == 1:
                        # 如果是字幕中间行且英文字幕无切分，则无中文字幕
                        subs[line_index].content = subs[line_index].content
                    else:
                        subs[line_index].content = subs[line_index].content + '\n' + '|'.join(tmp_parts)
                else:
                    subs[line_index].content = subs[line_index].content + '|' + '|'.join(tmp_parts)
                line_index = info.index
                tmp_parts = []
                if not info.is_blank and not flag:
                    flag = True
                    tmp_parts.append(trans_res[trans_index])
                    trans_index += 1
                else:
                    tmp_parts.append('')
    if len(subs[line_index].content.split('\n')) < 3:
        # 是否已经有第 3 行
        if len(tmp_parts) == 1 and tmp_parts[0] == '' and len(subs[line_index].content.split('|')) == 1:
            # 如果是字幕中间行且英文字幕无切分，则无中文字幕
            subs[line_index].content = subs[line_index].content
        else:
            subs[line_index].content = subs[line_index].content + '\n' + '|'.join(tmp_parts)
    else:
        subs[line_index].content = subs[line_index].content + '|' + '|'.join(tmp_parts)


def trans(subs, limit, trans_f, sleep_time=None):
    """
    将 subs 通过 trans_f 转换
    """
    for _ in get_sub_group(subs, limit):
        if sleep_time is not None:
            sleep(sleep_time)
        trans_group(subs, _, trans_f)
