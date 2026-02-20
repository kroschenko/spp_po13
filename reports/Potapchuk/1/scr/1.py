n = int(input("Введите количество чисел (N): "))

elements = list(map(int, input("Введите числа через пробел: ").split()))[:n]

unique_elements = list(set(elements))

print("Уникальные числа в последовательности:")

print(*unique_elements)
