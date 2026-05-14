def zadanie1():
    numbers = input("Введите числа: ").split()
    a = b = c = 0
    for n in numbers:
        if int(n) < 10 and int(n) > -10:
            a += 1
        elif int(n) < 100 and int(n) > -100:
            b += 1
        elif int(n) < 1000 and int(n) > -1000:
            c += 1
    print("Однозначных:", a)
    print("Двузначных:", b)
    print("Трехзначных:", c)
    return a, b, c


def zadanie2():
    results = []
    while True:
        text = input("Input: ")
        if text == "":
            break
        number = int(text)
        binary = bin(number)
        count = 0
        for symbol in binary:
            if symbol == "1":
                count = count + 1
        print("Output:", count)
        print()
        results.append(count)
    return results
