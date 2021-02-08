def get_valid_string(s):
    """
    只返回字符串 s 中的字母、数字组成的字符串
    """
    t = list(s)

    t = [_ for _ in t if _.isalnum()]

    res = ''.join(t)

    return res
