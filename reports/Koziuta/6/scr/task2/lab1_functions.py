def unique_numbers(numbers):
    """Return list of unique numbers from input list (preserve order of first appearance)."""
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    seen = set()
    result = []
    for n in numbers:
        if n not in seen:
            seen.add(n)
            result.append(n)
    return result

def add_binary(a: str, b: str) -> str:
    """Return sum of two binary strings as binary string."""
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("Both arguments must be strings")
    # Convert to integer, add, then back to binary without '0b'
    return bin(int(a, 2) + int(b, 2))[2:]
