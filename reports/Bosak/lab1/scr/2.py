def is_valid_brackets(bracket_string):
    brackets = {")": "(", "}": "{", "]": "["}
    stack = []

    for char in bracket_string:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack[-1] != brackets[char]:
                print(False)
                return
            stack.pop()

    print(len(stack) == 0)


def main():
    bracket_string = input()
    is_valid_brackets(bracket_string)


if __name__ == "__main__":
    main()
