a = input("Введите первое двоичное число (a): ") 
b = input("Введите второе двоичное число (b): ")

num_a = int(a, 2)
num_b = int(b, 2)

sum_decimal = num_a + num_b

result = bin(sum_decimal)[2:]

print(f"Результат сложения: {result}") 
