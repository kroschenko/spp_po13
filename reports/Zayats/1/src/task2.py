"""task2"""
# pylint: disable=duplicate-code
def is_brackets_correct(s: str) -> bool:
    """Проверка корректности скобок."""
    stack = []

    pairs = {')': '(', ']': '[', '}': '{'}

    for c in s:
        if c in "([{":
            stack.append(c)
        elif c in ")]}":
            if not stack:
                return False

            last = stack.pop()
            if pairs[c] != last:
                return False

    return len(stack) == 0


def run():
    """Запуск программы."""
    s = input("Введите строку: ")
    print(is_brackets_correct(s))


if __name__ == "__main__":
    run()
