from typing import List, Tuple


def get_list_diff(l1: List[str], l2: List[str]) -> Tuple[int, int, int, int]:
    """
    返回列表 l1 中与 l2 不同的地方

    返回的元组：
    第一个是 l1 差异起始位置，
    第二个是 l1 差异结束位置（不包含），
    第三个是 l2 差异起始位置，
    第四个是 l2 差异结束位置（不包含）
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
                    res.append((d1, i1+1, d2, i2+1))
                    in_diff = False
                    i1 += 1
                    i2 += 1
                else:
                    # 继续处理 diff
                    if len(''.join(l1[d1:i1+1])) > len(''.join(l2[d2:i2+1])):
                        i2 += 1
                    else:
                        i1 += 1
    return res
