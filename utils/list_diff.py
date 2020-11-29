from enum import Enum
from typing import List, Tuple


class ListDiffType(Enum):
    """
    EXPAND 表示需要展开；
    MERGE 表示需要合并。
    """
    EXPAND = 0
    MERGE = 1


def get_list_diff(l1: List[str], l2: List[str]) -> Tuple[ListDiffType, int, int]:
    """
    返回列表 l1 中与 l2 不同的地方

    返回的元组，第一个是差异类型，第二个是差异起始位置，第三个是差异持续个数
    """
    i1 = i2 = 0
    d1 = d2 = None  # diff 起始位置
    in_diff = False  # 在差异处理过程中

    res = []

    while i1 < len(l1) and i2 < len(l2):
        # print(i1, i2)
        if l1[i1] == l2[i2]:
            i1 += 1
            i2 += 1
        else:
            # 如果当前值不相等
            if not in_diff:
                # diff 开始
                # print('not in_diff {} {}'.format(i1, i2))
                d1, d2 = i1, i2  # 记录差异起始位置
                if len(l1[i1]) > len(l2[i2]):
                    i2 += 1
                else:
                    i1 += 1
                in_diff = True
            else:
                # diff 处理中
                if ''.join(l1[d1:i1+1]) == ''.join(l2[d2:i2+1]):
                    # 累积字符串相等， diff 结束
                    if i1 == d1:
                        res.append((ListDiffType.EXPAND, d1, i2+1-d2))
                    else:
                        res.append((ListDiffType.MERGE, d1, i1+1-d1))
                    in_diff = False
                    i1 += 1
                    i2 += 1
                else:
                    # 继续处理 diff
                    if i1 == d1:
                        i2 += 1
                    else:
                        i1 += 1
    return res
