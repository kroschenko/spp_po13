def sum_squares_negative(numbers_list):
    return sum(x**2 for x in numbers_list if x < 0)


def main():
    numbers = list(map(int, input().split()))
    result = sum_squares_negative(numbers)
    print(result)


if __name__ == "__main__":
    main()
