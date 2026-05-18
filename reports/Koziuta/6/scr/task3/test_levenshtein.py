import pytest
from levenshtein import levenshtein_distance

def test_both_none():
    with pytest.raises(TypeError):
        levenshtein_distance(None, None)

def test_first_none():
    assert levenshtein_distance(None, "abc") == -1

def test_second_none():
    assert levenshtein_distance("abc", None) == -1

def test_empty_strings():
    assert levenshtein_distance("", "") == 0

def test_empty_vs_string():
    assert levenshtein_distance("", "a") == 1
    assert levenshtein_distance("", "aaapppp") == 7

def test_spaces_examples():
    # Spec tests with spaces (note: actual strings include spaces)
    assert levenshtein_distance(" frog ", " fog ") == 1
    assert levenshtein_distance("fly", " ant ") == 3
    assert levenshtein_distance(" elephant ", " hippo ") == 7
    assert levenshtein_distance(" hippo ", " elephant ") == 7
    assert levenshtein_distance(" hippo ", " zzzzzzzz ") == 8

def test_hello_hallo():
    assert levenshtein_distance(" hello ", " hallo ") == 1

def test_normal_words():
    assert levenshtein_distance("kitten", "sitting") == 3
    assert levenshtein_distance("flaw", "lawn") == 2
