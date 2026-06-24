"""String loose function module."""

def loose(string, remove):
    """Remove all characters from first string that appear in second."""
    if string is None and remove is None:
        raise TypeError
    if string is None:
        return None
    if remove is None:
        return string
    if not isinstance(string, str) or not isinstance(remove, str):
        raise TypeError("Both arguments must be strings")
    if string == "":
        return ""
    if remove == "":
        return string

    remove_set = set(remove)
    result = "".join(char for char in string if char not in remove_set)
    return result
