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


if __name__ == "__main__":
    print(generate_random_sequence(5))
    print(find_majority_element([1, 2, 2, 2, 3]))
