from lab1 import generate_random_sequence, find_majority_element


class TestGenerateRandomSequence:
    def test_length(self):
        result = generate_random_sequence(5)
        assert len(result) == 5

    def test_contains_all_numbers(self):
        result = generate_random_sequence(5)
        assert sorted(result) == [1, 2, 3, 4, 5]

    def test_zero_n(self):
        result = generate_random_sequence(0)
        assert not result

    def test_one_element(self):
        result = generate_random_sequence(1)
        assert result == [1]


class TestFindMajorityElement:
    def test_majority_exists(self):
        assert find_majority_element([3, 2, 3]) == 3

    def test_majority_exists_long(self):
        assert find_majority_element([2, 2, 1, 1, 1, 2, 2]) == 2

    def test_no_majority(self):
        assert find_majority_element([1, 2, 3, 4]) is None

    def test_single_element(self):
        assert find_majority_element([1]) == 1

    def test_two_elements_same(self):
        assert find_majority_element([1, 1]) == 1

    def test_two_elements_different(self):
        assert find_majority_element([1, 2]) is None

    def test_empty_list(self):
        assert find_majority_element([]) is None

    def test_all_same(self):
        assert find_majority_element([5, 5, 5, 5, 5]) == 5
