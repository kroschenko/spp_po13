numbers = []
print("Вводите числа (для завершения нажмите Enter без ввода):")

while True:
    user_input = input("Число: ")
    if user_input == "":
        break
    try:
        num = int(user_input)
        numbers.append(num)
    except ValueError:
        print("Ошибка! Введите целое число.")

sum_squares = sum(x**2 for x in numbers if x < 0)

print(f"\nВведенные числа: {numbers}")
print(f"Сумма квадратов отрицательных чисел: {sum_squares}")