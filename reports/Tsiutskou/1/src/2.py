nums = list(map(int, input("Введите числа: ").split()))
for x in set(nums):
    if nums.count(x) > len(nums) // 2:
        print(f"Элемент большинства: {x}")
        break
else:
    print("Нет элемента большинства")
