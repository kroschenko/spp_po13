def hamming_distance(str1, str2):
    if str1 is None and str2 is None:
        raise TypeError
    if str1 is None or str2 is None:
        return -1
    if not isinstance(str1, str) or not isinstance(str2, str):
        return -1
    if len(str1) != len(str2):
        raise ValueError
    distance = 0
    for i, char in enumerate(str1):
        if char != str2[i]:
            distance += 1
    return distance
