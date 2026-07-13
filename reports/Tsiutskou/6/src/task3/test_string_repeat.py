import pytest
from string_repeat import repeat


def test_zero_repeat():
    assert repeat("e", "|", 0) == ""


def test_three_repeat():
    assert repeat("e", "|", 3) == "e|e|e"


def test_with_spaces():
    assert repeat(" ABC ", ",", 2) == "ABC,ABC"


def test_empty_separator():
    assert repeat(" DBE ", "", 2) == "DBEDBE"


def test_one_repeat():
    assert repeat(" DBE ", ":", 1) == "DBE"


def test_negative_repeat():
    with pytest.raises(ValueError):
        repeat("e", "|", -2)


def test_empty_string():
    assert repeat("", ":", 3) == "::"


def test_none_pattern():
    with pytest.raises(TypeError):
        repeat(None, "a", 1)


def test_none_separator():
    with pytest.raises(TypeError):
        repeat("a", None, 2)
