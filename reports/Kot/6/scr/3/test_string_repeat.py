import sys
import time
import pytest
from string_repeat import repeat


class TestStringRepeatCore:
    """
    Core tests for repeat function - normal cases and basic functionality
    """

    # === Tests for normal cases ===

    def test_repeat_with_zero_repetitions(self):
        """Test: repeat(pattern, 0) should return empty string"""
        assert repeat("e", 0) == ""
        assert repeat("abc", 0) == ""
        assert repeat("123", 0) == ""

    def test_repeat_with_positive_repetitions(self):
        """Test: repeat(pattern, positive number) should return repeated pattern"""
        assert repeat("e", 3) == "eee"
        assert repeat("ab", 2) == "abab"
        assert repeat("123", 1) == "123"
        assert repeat(" ", 3) == "   "
        assert repeat("!@#", 2) == "!@#!@#"

    def test_repeat_with_multiple_characters(self):
        """Test: repeat with patterns containing multiple characters"""
        assert repeat(" ABC ", 2) == " ABC  ABC "
        assert repeat("Hello", 3) == "HelloHelloHello"
        assert repeat("Test ", 2) == "Test Test "
        assert repeat("--->", 4) == "--->--->--->--->"

    def test_repeat_with_single_character(self):
        """Test: repeat with single character patterns"""
        assert repeat("a", 5) == "aaaaa"
        assert repeat("x", 10) == "xxxxxxxxxx"
        assert repeat("1", 3) == "111"

    def test_repeat_with_whitespace(self):
        """Test: repeat with whitespace patterns"""
        assert repeat(" ", 5) == "     "
        assert repeat("\t", 2) == "\t\t"
        assert repeat("\n", 3) == "\n\n\n"
        assert repeat(" \t ", 2) == " \t  \t "

    def test_repeat_with_special_characters(self):
        """Test: repeat with special characters"""
        assert repeat("!@#$%", 2) == "!@#$%!@#$%"
        assert repeat("\\n", 3) == "\\n\\n\\n"
        assert repeat("'\"", 2) == "'\"'\""

    def test_repeat_with_unicode(self):
        """Test: repeat with unicode characters"""
        assert repeat("Привет", 2) == "ПриветПривет"
        assert repeat("😊", 3) == "😊😊😊"
        assert repeat("★", 4) == "★★★★"
        assert repeat("ño", 2) == "ñoño"


class TestStringRepeatErrors:
    """Error handling tests for repeat function"""

    def test_repeat_with_negative_repetitions_raises_value_error(self):
        """Test: repeat(pattern, negative) should raise ValueError"""
        with pytest.raises(ValueError, match="repeat count must be non-negative"):
            repeat("e", -1)

        with pytest.raises(ValueError, match="repeat count must be non-negative"):
            repeat("abc", -5)

        with pytest.raises(ValueError):
            repeat("test", -2)

    def test_repeat_with_none_pattern_raises_type_error(self):
        """Test: repeat(None, n) should raise TypeError"""
        with pytest.raises(TypeError, match="pattern must be a string"):
            repeat(None, 1)

        with pytest.raises(TypeError):
            repeat(None, 5)

    def test_repeat_with_non_string_pattern_raises_type_error(self):
        """Test: repeat(non-string, n) should raise TypeError"""
        with pytest.raises(TypeError, match="pattern must be a string"):
            repeat(123, 3)

        with pytest.raises(TypeError, match="pattern must be a string"):
            repeat(3.14, 2)

        with pytest.raises(TypeError):
            repeat([1, 2, 3], 2)

        with pytest.raises(TypeError):
            repeat({"key": "value"}, 1)

    def test_repeat_with_non_integer_repetitions_raises_type_error(self):
        """Test: repeat(pattern, non-integer) should raise TypeError"""
        with pytest.raises(TypeError, match="repeat count must be an integer"):
            repeat("abc", "2")

        with pytest.raises(TypeError, match="repeat count must be an integer"):
            repeat("abc", 3.5)

        with pytest.raises(TypeError):
            repeat("abc", [1])


class TestStringRepeatParameterized:
    """Parameterized tests for repeat function"""

    @pytest.mark.parametrize(
        "pattern,repetitions,expected",
        [
            ("e", 0, ""),
            ("e", 1, "e"),
            ("e", 3, "eee"),
            ("abc", 2, "abcabc"),
            (" ABC ", 2, " ABC  ABC "),
            ("", 5, ""),
            ("a", 1, "a"),
            ("ab", 3, "ababab"),
            ("123", 0, ""),
            ("!@#", 2, "!@#!@#"),
            ("\n", 2, "\n\n"),
            ("😊", 3, "😊😊😊"),
            ("Привет", 1, "Привет"),
            (" ", 3, "   "),
            (" x ", 2, " x  x "),
        ],
    )
    def test_repeat_parameterized(self, pattern, repetitions, expected):
        """Parameterized test for various valid inputs"""
        result = repeat(pattern, repetitions)
        assert result == expected, f"Expected '{expected}', got '{result}'"

    @pytest.mark.parametrize(
        "pattern,repetitions,expected_exception,expected_message",
        [
            ("e", -1, ValueError, "repeat count must be non-negative"),
            ("abc", -5, ValueError, "repeat count must be non-negative"),
            (None, 1, TypeError, "pattern must be a string"),
            (123, 3, TypeError, "pattern must be a string"),
            (3.14, 2, TypeError, "pattern must be a string"),
            ("abc", "2", TypeError, "repeat count must be an integer"),
            ("abc", 3.5, TypeError, "repeat count must be an integer"),
        ],
    )
    def test_repeat_error_cases_parameterized(
        self, pattern, repetitions, expected_exception, expected_message
    ):
        """Parameterized test for various error cases"""
        with pytest.raises(expected_exception, match=expected_message):
            repeat(pattern, repetitions)


class TestStringRepeatEdgeCases:
    """Edge cases for repeat function"""

    def test_repeat_with_empty_string_pattern(self):
        """Test: repeat("", n) should return empty string for any n >= 0"""
        assert repeat("", 0) == ""
        assert repeat("", 5) == ""
        assert repeat("", 100) == ""

    def test_repeat_with_large_repetitions(self):
        """Test: repeat with large number of repetitions"""
        pattern = "a"
        repetitions = 10000
        result = repeat(pattern, repetitions)
        assert len(result) == repetitions
        assert result == "a" * repetitions

    def test_repeat_with_complex_pattern(self):
        """Test: repeat with complex pattern"""
        pattern = "A B C"
        assert repeat(pattern, 3) == "A B CA B CA B C"
        assert repeat(pattern, 1) == "A B C"

    def test_repeat_with_pattern_containing_newlines(self):
        """Test: repeat with pattern containing newlines"""
        pattern = "Line1\n"
        assert repeat(pattern, 3) == "Line1\nLine1\nLine1\n"

    def test_concatenation_behavior(self):
        """Demonstrate string concatenation behavior"""
        pattern = " ABC "
        assert pattern * 2 == " ABC  ABC "
        assert list(pattern) == [" ", "A", "B", "C", " "]


class TestStringRepeatSpecification:
    """Tests for exact specification requirements"""

    def test_specification_example_1(self):
        """Test specification example: repeat("e", 0) = "" """
        assert repeat("e", 0) == ""

    def test_specification_example_2(self):
        """Test specification example: repeat("e", 3) = "eee" """
        assert repeat("e", 3) == "eee"

    def test_specification_example_3(self):
        """Test specification example: repeat(" ABC ", 2) = " ABC  ABC " """
        assert repeat(" ABC ", 2) == " ABC  ABC "

    def test_specification_example_4(self):
        """Test specification example: repeat("e", -2) = ValueError"""
        with pytest.raises(ValueError):
            repeat("e", -2)

    def test_specification_example_5(self):
        """Test specification example: repeat(None, 1) = TypeError"""
        with pytest.raises(TypeError):
            repeat(None, 1)

    def test_all_specification_requirements(self):
        """Test all requirements from the specification with corrected expectations"""
        assert repeat("e", 0) == ""
        assert repeat("e", 3) == "eee"
        assert repeat(" ABC ", 2) == " ABC  ABC "

        with pytest.raises(ValueError):
            repeat("e", -2)

        with pytest.raises(TypeError):
            repeat(None, 1)


class TestStringRepeatPerformance:
    """Performance tests for repeat function"""

    def test_repeat_performance_with_large_repetitions(self):
        """Test performance with large repetitions"""
        pattern = "test"
        repetitions = 100000

        start_time = time.time()
        result = repeat(pattern, repetitions)
        end_time = time.time()

        assert len(result) == len(pattern) * repetitions
        assert end_time - start_time < 1.0

    def test_memory_efficiency(self):
        """Test that function doesn't use excessive memory"""
        pattern = "x"
        repetitions = 1000000
        result = repeat(pattern, repetitions)

        expected_size = repetitions
        actual_size = sys.getsizeof(result)

        assert actual_size < expected_size * 1.5


# === Educational tests (not counted as class methods) ===


def test_understanding_string_multiplication():
    """Educational test to understand how string multiplication works"""
    assert "ABC" * 3 == "ABCABCABC"
    assert " A " * 2 == " A  A "
    pattern = "  Hello  "
    assert pattern * 2 == "  Hello    Hello  "
    assert "" * 100 == ""
    assert "x" * 5 == "xxxxx"


def test_educational_demonstration():
    """Educational test to demonstrate the behavior"""
    print("\n" + "=" * 60)
    print("String Repeat Educational Demo")
    print("=" * 60)

    examples = [
        ('"e" * 0', "", ""),
        ('"e" * 3', "eee", "eee"),
        ('" ABC " * 2', " ABC  ABC ", " ABC  ABC "),
    ]

    for desc, expected, result in examples:
        print(f"\n{desc}:")
        print(f"  Expected: '{expected}'")
        print(f"  Result: '{result}'")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Running String Repeat Tests")
    print("=" * 60 + "\n")

    exit_code = pytest.main([__file__, "-v", "-s", "--tb=short"])

    print("\n" + "=" * 60)
    if exit_code == 0:
        print("✓ All tests passed successfully!")
    else:
        print(f"✗ Tests failed with exit code: {exit_code}")
    print("=" * 60)

    input("\nPress Enter to exit...")
    sys.exit(exit_code)
