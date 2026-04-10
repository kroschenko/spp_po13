def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None


# Ввод данных
nums = list(map(int, input("Введите числа через пробел: ").split()))
target = int(input("Введите целевое число: "))

result = two_sum(nums, target)
if result:
    print(f"Индексы: {result}")
    print(f"Проверка: {nums[result[0]]} + {nums[result[1]]} = {target}")
else:
    print("Решение не найдено")
