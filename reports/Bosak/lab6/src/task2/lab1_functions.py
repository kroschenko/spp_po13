"""Functions from laboratory work 1."""

def sum_squares_negative(numbers):
    """Return sum of squares of negative numbers."""
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    return sum(x ** 2 for x in numbers if x < 0)


def is_valid_brackets(s):
    """Check if brackets string is valid."""
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    pairs = {")": "(", "}": "{", "]": "["}
    stack = []
    for char in s:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    return len(stack) == 0
