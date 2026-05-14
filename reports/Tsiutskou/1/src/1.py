import random

N = int(input("Введите количество чисел N: "))
numbers = list(range(1, N + 1))
random.shuffle(numbers)
print(f"\n{N} чисел в случайном порядке:")
print(" ".join(map(str, numbers)))
