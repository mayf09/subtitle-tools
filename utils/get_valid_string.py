def get_valid_string(s):
    """
    返回字符串 s 中的字母、数字、 % 组成的字符串
    """
    t = list(s)

    t = [_ for _ in t if _.isalnum() or _ == '%']

    res = ''.join(t)

    return res
