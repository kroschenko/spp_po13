def repeat(str, separator, repeat):
    if str is None or separator is None:
        raise TypeError("Arguments cannot be None")

    if repeat < 0:
        raise ValueError("Repeat count cannot be negative")

    if repeat == 0:
        return ""

    str_clean = str.strip()

    if repeat == 1:
        return str_clean

    result = str_clean
    for i in range(repeat - 1):
        result += separator + str_clean

    return result
