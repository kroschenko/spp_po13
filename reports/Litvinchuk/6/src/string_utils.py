"""Utility functions for string processing."""


def keep(string, pattern):
    """Keep characters from string that are present in pattern, preserving spaces."""
    if string is None and pattern is None:
        raise TypeError("Both arguments are None")

    if string is None:
        return None

    if string == "":
        return ""

    if pattern is None or pattern == "":
        return ""

    result = ""

    for char in string:
        if char in pattern or char == " ":
            result += char

    return result
