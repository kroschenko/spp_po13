"""test proj 3"""
# pylint: disable=import-error
import pytest # type: ignore
from loose import loose


#  ТЕСТЫ ПО СПЕЦИФИКАЦИИ
def test_loose_none_none():
    """test"""
    with pytest.raises(TypeError):
        loose(None, None)


def test_loose_none_any():
    """test"""
    assert loose(None, "abc") is None


def test_loose_empty_any():
    """test"""
    assert loose("", "abc") == ""


def test_loose_any_none():
    """test"""
    assert loose("hello", None) == "hello"


def test_loose_any_empty():
    """test"""
    assert loose("hello", "") == "hello"


def test_loose_example_1():
    """test"""
    assert loose(" hello ", "hl") == "eo"


def test_loose_example_2():
    """test"""
    assert loose(" hello ", "le") == "ho"

def test_loose_no_common_chars():
    """test"""
    assert loose("abc", "xyz") == "abc"


def test_loose_remove_all():
    """test"""
    assert loose("aaa", "a") == ""


def test_loose_case_sensitive():
    """test"""
    assert loose("AaA", "a") == "AA"   # 'a' != 'A'


def test_loose_non_string_first():
    """test"""
    with pytest.raises(TypeError):
        loose(123, "abc")


def test_loose_non_string_second():
    """test"""
    with pytest.raises(TypeError):
        loose("abc", 123)
