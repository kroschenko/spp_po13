# string_repeat.py


def repeat(pattern, repetitions):
    """Efficient string repetition using multiplication operator."""
    # Check pattern type
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")

    # Check repetitions type
    if not isinstance(repetitions, int):
        raise TypeError("repeat count must be an integer")

    # Check repetitions value
    if repetitions < 0:
        raise ValueError("repeat count must be non-negative")

    # Use string multiplication for efficient repetition
    return pattern * repetitions


def repeat_explicit(input_pattern, repeat_count):
    """
    Alternative implementation showing concatenation process.

    Args:
        input_pattern: String pattern to repeat
        repeat_count: Number of repetitions (non-negative integer)
    """
    if not isinstance(input_pattern, str):
        raise TypeError("pattern must be a string")

    if not isinstance(repeat_count, int):
        raise TypeError("repeat count must be an integer")

    if repeat_count < 0:
        raise ValueError("repeat count must be non-negative")

    concatenated_result = ""
    for step_index in range(repeat_count):
        concatenated_result += input_pattern
        # Debug output to show concatenation process
        print(f"Step {step_index + 1}: result = '{concatenated_result}'")

    return concatenated_result


def repeat_with_debug(input_pattern, repeat_count):
    """Function with debug output to demonstrate string repetition."""
    if not isinstance(input_pattern, str):
        raise TypeError("pattern must be a string")

    if not isinstance(repeat_count, int):
        raise TypeError("repeat count must be an integer")

    if repeat_count < 0:
        raise ValueError("repeat count must be non-negative")

    print("Pattern: '{}' (length: {})".format(input_pattern, len(input_pattern)))
    print("Repetitions: {}".format(repeat_count))

    final_result = input_pattern * repeat_count

    print("Result: '{}'".format(final_result))
    print("Result length: {}".format(len(final_result)))

    # Show character by character breakdown
    print("Character breakdown:")
    for position, current_char in enumerate(final_result):
        ascii_val = ord(current_char) if ord(current_char) < 128 else "unicode"
        print(
            "  Position {}: '{}' (ASCII: {})".format(position, current_char, ascii_val)
        )

    return final_result


if __name__ == "__main__":
    print("String Repeat Module")
    print("=" * 60)

    # Test examples from specification
    print("\n1. Testing specification examples:")
    print('  repeat("e", 0) = "{}"'.format(repeat("e", 0)))
    print('  repeat("e", 3) = "{}"'.format(repeat("e", 3)))
    print('  repeat(" ABC ", 2) = "{}"'.format(repeat(" ABC ", 2)))

    # Test with debug to understand the issue
    print("\n2. Debug mode for ' ABC ' pattern:")
    repeat_with_debug(" ABC ", 2)

    print("\n3. Explicit concatenation demonstration:")
    repeat_explicit(" ABC ", 2)

    # Test error cases
    print("\n4. Testing error cases:")
    try:
        repeat("e", -2)
    except ValueError as err:
        print('  repeat("e", -2) -> ValueError: {}'.format(err))

    try:
        repeat(None, 1)
    except TypeError as err:
        print("  repeat(None, 1) -> TypeError: {}".format(err))

    print("\n5. Understanding the result:")
    test_pattern = " ABC "
    test_result = repeat(test_pattern, 2)
    print('  Pattern: "{}"'.format(test_pattern))
    print('  Result: "{}"'.format(test_result))
    print('  Expected: " ABC  ABC "')
    print("  Are they equal? {}".format(test_result == " ABC  ABC "))
    print("  Result characters:")
    for idx, ch in enumerate(test_result):
        print('    {}: "{}"'.format(idx, ch))
