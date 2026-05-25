def repeat_string(input_str, separator, repeat_count):
    if input_str is None or separator is None:
        raise TypeError("Arguments cannot be None")

    if repeat_count < 0:
        raise ValueError("Repeat count cannot be negative")

    if repeat_count == 0:
        return ""

    str_clean = input_str.strip()

    if repeat_count == 1:
        return str_clean

    result = str_clean
    for _ in range(repeat_count - 1):
        result += separator + str_clean

    return result
