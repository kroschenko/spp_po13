import random
from datetime import datetime

class File:
    def __init__(self, name, size, ext):
        self.name = name
        self.size = size
        self.ext = ext
        self.created = datetime.now()
    
    def __str__(self):
        return f"Файл: {self.name}.{self.ext}, размер: {self.size}KB, создан: {self.created.date()}"

class Directory:
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def add(self, component):
        self.children.append(component)
    
    def get_size(self):
        return sum(c.size if isinstance(c, File) else c.get_size() for c in self.children)
    
    def __str__(self):
        return f"Папка: {self.name}, размер: {self.get_size()}KB"

def collect_all(component, result):
    result.append(component)
    if isinstance(component, Directory):
        for child in component.children:
            collect_all(child, result)
    return result

print("=== Создание файловой системы ===")
root = Directory(input("Имя корневой папки: "))

while True:
    print("\n1 - Добавить папку")
    print("2 - Добавить файл")
    print("3 - Закончить создание ФС")
    choice = input("Выбор: ")
    
    if choice == "1":
        name = input("Имя папки: ")
        root.add(Directory(name))
    
    elif choice == "2":
        name = input("Имя файла: ")
        size = int(input("Размер (KB): "))
        ext = input("Расширение: ")
        root.add(File(name, size, ext))
    
    elif choice == "3":
        break

all_items = collect_all(root, [])

print("\n=== Обычный порядок вывода ===")
for item in all_items:
    print(item)

print("\n=== Случайный порядок вывода ===")
random.shuffle(all_items)
for item in all_items:
    print(item)