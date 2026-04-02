# string_repeat.py


def repeat(pattern, repetitions):
    # Check pattern type
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")

    # Check repetitions type
    if not isinstance(repetitions, int):
        raise TypeError("repeat count must be an integer")

    # Check repetitions value
    if repetitions < 0:
        raise ValueError("repeat count must be non-negative")

    # Optimization for common cases
    if repetitions == 0:
        return ""

    if repetitions == 1:
        return pattern

    # Use string multiplication for efficient repetition
    # This is the most efficient way in Python
    return pattern * repetitions


# Альтернативная реализация, которая показывает процесс конкатенации
def repeat_explicit(pattern, repetitions):
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")

    if not isinstance(repetitions, int):
        raise TypeError("repeat count must be an integer")

    if repetitions < 0:
        raise ValueError("repeat count must be non-negative")

    result = ""
    for i in range(repetitions):
        result += pattern
        # Debug output to show concatenation process
        print(f"Step {i+1}: result = '{result}'")

    return result


# Функция для демонстрации работы с отладкой
def repeat_with_debug(pattern, repetitions):
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")

    if not isinstance(repetitions, int):
        raise TypeError("repeat count must be an integer")

    if repetitions < 0:
        raise ValueError("repeat count must be non-negative")

    print(f"Pattern: '{pattern}' (length: {len(pattern)})")
    print(f"Repetitions: {repetitions}")

    result = pattern * repetitions

    print(f"Result: '{result}'")
    print(f"Result length: {len(result)}")

    # Show character by character breakdown
    print("Character breakdown:")
    for i, char in enumerate(result):
        print(
            f"  Position {i}: '{char}' (ASCII: {ord(char) if ord(char) < 128 else 'unicode'})"
        )

    return result


if __name__ == "__main__":
    print("String Repeat Module")
    print("=" * 60)

    # Test examples from specification
    print("\n1. Testing specification examples:")
    print(f'  repeat("e", 0) = "{repeat("e", 0)}"')
    print(f'  repeat("e", 3) = "{repeat("e", 3)}"')
    print(f'  repeat(" ABC ", 2) = "{repeat(" ABC ", 2)}"')

    # Test with debug to understand the issue
    print("\n2. Debug mode for ' ABC ' pattern:")
    repeat_with_debug(" ABC ", 2)

    print("\n3. Explicit concatenation demonstration:")
    repeat_explicit(" ABC ", 2)

    # Test error cases
    print("\n4. Testing error cases:")
    try:
        repeat("e", -2)
    except ValueError as e:
        print(f'  repeat("e", -2) -> ValueError: {e}')

    try:
        repeat(None, 1)
    except TypeError as e:
        print(f"  repeat(None, 1) -> TypeError: {e}")

    print("\n5. Understanding the result:")
    pattern = " ABC "
    result = repeat(pattern, 2)
    print(f'  Pattern: "{pattern}"')
    print(f'  Result: "{result}"')
    print(f'  Expected: " ABCABC "')
    print(f'  Are they equal? {result == " ABCABC "}')
    print(f"  Result characters:")
    for i, char in enumerate(result):
        print(f'    {i}: "{char}"')
