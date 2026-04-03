s = input("Введите строку: ")
stack = []
FLAG = True

for c in s:
    if c in ('(', '[', '{'):
        stack.append(c)
    else:
        if not stack:
            FLAG = False
            break

        last = stack.pop()

        if (c, last) not in {(')', '('), (']', '['), ('}', '{')}:
            FLAG = False
            break

if stack:
    FLAG = False

print(FLAG)