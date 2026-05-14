import random


def generate_random_sequence(n):
    numbers = list(range(1, n + 1))
    random.shuffle(numbers)
    return numbers


def find_majority_element(nums):
    for x in set(nums):
        if nums.count(x) > len(nums) // 2:
            return x
    return None
