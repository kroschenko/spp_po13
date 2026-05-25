import pytest
from string_repeat import repeat_string


def test_zero_repeat():
    assert repeat_string("e", "|", 0) == ""


def test_three_repeat():
    assert repeat_string("e", "|", 3) == "e|e|e"


def test_with_spaces():
    assert repeat_string(" ABC ", ",", 2) == "ABC,ABC"


def test_empty_separator():
    assert repeat_string(" DBE ", "", 2) == "DBEDBE"


def test_one_repeat():
    assert repeat_string(" DBE ", ":", 1) == "DBE"


def test_negative_repeat():
    with pytest.raises(ValueError):
        repeat_string("e", "|", -2)


def test_empty_string():
    assert repeat_string("", ":", 3) == "::"


def test_none_pattern():
    with pytest.raises(TypeError):
        repeat_string(None, "a", 1)


def test_none_separator():
    with pytest.raises(TypeError):
        repeat_string("a", None, 2)
