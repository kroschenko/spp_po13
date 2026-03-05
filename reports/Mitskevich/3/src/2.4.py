from abc import ABC, abstractmethod


class FileSystemComponent(ABC):
    """Абстрактный базовый класс для всех компонентов файловой системы"""

    def __init__(self, name, date):
        self._name = name
        self._date = date

    @abstractmethod
    def getSize(self):
        pass

    @abstractmethod
    def display(self, indent=""):
        pass

    def getName(self):
        return self._name

    def getDate(self):
        return self._date

    def add(self, component):
        raise NotImplementedError("Сюда добавлять текст низя :( )")

    def remove(self, component):
        raise NotImplementedError("Удалить низя :( )")

    def getChild(self, index):
        raise NotImplementedError("Упс, что-то пошло не так *_* ")


"""Класс папочки"""


class Directory(FileSystemComponent):

    def __init__(self, name, date):
        super().__init__(name, date)
        self._children = []

    def add(self, component):
        """Добавление компонента в директорию"""
        if component not in self._children:
            self._children.append(component)
            print(f"{component.getName()} добавлен в папочку {self._name}")
        else:
            print(f"{component.getName()} уже есть в папочке {self._name}")

    def remove(self, component):
        """Удаление компонента из директории"""
        if component in self._children:
            self._children.remove(component)
            print(f"{component.getName()} удален из папочки {self._name}, дасвиданя ;)")

    def getChild(self, index):
        """Получение дочернего компонента по индексу"""
        if 0 <= index < len(self._children):
            return self._children[index]
        return None

    def getChildren(self):
        """Получение всех дочерних компонентов"""
        return self._children.copy()

    def getSize(self):
        """Рекурсивный подсчет размера папки"""
        total_size = 0
        for child in self._children:
            total_size += child.getSize()
        return total_size

    def findByName(self, name):
        """Поиск компонента по имени в текущей папке"""
        for child in self._children:
            if child.getName() == name:
                return child
        return None

    def display(self, indent=""):
        """Вывод содержимого папки"""
        print(
            f"{indent}{self._name}/ (размер: {self.getSize()} байт, создан: {self._date})"
        )
        for child in self._children:
            child.display(indent + "  ")


"""Класс файл"""


class File(FileSystemComponent):

    def __init__(self, name, extension, date):
        super().__init__(f"{name}.{extension}", date)
        self._name_without_ext = name
        self._extension = extension
        self._size = 0
        self._content = ""

    def getSize(self):
        return self._size

    def getExtension(self):
        return self._extension

    def addContent(self):
        """Добавление содержимого в файл"""
        if self._extension.lower() == "txt":
            contOfFile = input("Введите содержимое текстового файла: ")
            self._content = contOfFile
            self._size = len(contOfFile.encode("utf-8"))  # Размер в байтах
            print(
                f"Содержимое добавлено в файл {self._name}. Размер: {self._size} байт"
            )
        else:
            print(
                f"Это не текстовый файл (расширение .{self._extension}), вводить низя :("
            )

    def readContent(self):
        """Чтение содержимого файла"""
        if self._extension.lower() == "txt" and self._content:
            print(f"\nСодержимое файла {self._name}:")
            print(self._content)
            print()
        elif self._extension.lower() == "txt":
            print(f"Файл {self._name} пуст")
        else:
            print(f"Файл {self._name} - бинарный, прочитать как текст низя :( )")

    def display(self, indent=""):
        """Отображение информации о файле"""
        print(
            f"{indent} {self._name} (размер: {self._size} байт, создан: {self._date})"
        )


"""Класс для управления файловой системой в целом"""


class FileSystem:

    def __init__(self):
        # При создании корня просим пользователя ввести дату
        root_date = input(
            "Введите дату создания корневой директории (например, 2024-01-15): "
        )
        self._root = Directory("root", root_date)
        self._current_directory = self._root
        self._current_path = ["root"]

    def getCurrentPath(self):
        """Получение текущего пути"""
        return "/" + "/".join(self._current_path)

    def changeDirectory(self, dirname):
        """Смена текущей директории"""
        if dirname == "..":
            if len(self._current_path) > 1:
                self._current_path.pop()
                # Перестроение текущей директории от корня
                self._current_directory = self._root
                for dir_name in self._current_path[1:]:
                    next_dir = self._current_directory.findByName(dir_name)
                    if next_dir and isinstance(next_dir, Directory):
                        self._current_directory = next_dir
                    else:
                        break
                print(f"Перешли в директорию {self.getCurrentPath()}")
            else:
                print("Уже в корневой директории")
        else:
            # Поиск поддиректории в текущей
            target = self._current_directory.findByName(dirname)
            if target and isinstance(target, Directory):
                self._current_directory = target
                self._current_path.append(dirname)
                print(f"Перешли в папочку {self.getCurrentPath()}")
            else:
                print(f"Папка '{dirname}' не найдена, плак плак ((( )")

    def createFile(self, name, extension):
        """Создание файла в текущей папке"""
        # Проверка на существование файла с таким именем
        filename = f"{name}.{extension}"
        existing = self._current_directory.findByName(filename)
        if existing:
            print(f"Файл '{filename}' уже существует")
            return None

        # Просим пользователя ввести дату создания файла
        file_date = input(f"Введите дату создания файла {filename}: ")
        new_file = File(name, extension, file_date)
        self._current_directory.add(new_file)
        return new_file

    def createDirectory(self, name):
        """Создание папки в папке"""
        existing = self._current_directory.findByName(name)
        if existing:
            print(f"Папка '{name}' уже существует")
            return None

        # Просим пользователя ввести дату создания папки
        dir_date = input(f"Введите дату создания папки {name}: ")
        new_dir = Directory(name, dir_date)
        self._current_directory.add(new_dir)
        return new_dir

    def listContents(self):
        """Вывод содержимого текущей папки"""
        print(f"\nСодержимое {self.getCurrentPath()}:")
        if not self._current_directory.getChildren():
            print("  (пусто, выросла капуста, хы)")
        else:
            self._current_directory.display()

    def findFile(self, filename):
        """Поиск файла в текущей папке"""
        return self._current_directory.findByName(filename)

    def deleteItem(self, name):
        """Удаление файла или папки из текущей папки"""
        item = self._current_directory.findByName(name)
        if item:
            self._current_directory.remove(item)
        else:
            print(f"'{name}' не найден в текущей папке, какой ужассс")

    def getCurrentDirectory(self):
        """Получение объекта текущей папки"""
        return self._current_directory


def Menu():
    print("*" * 50)
    print("Команды:")
    print("  ls              - показать содержимое текущей директории")
    print("  cd <директория> - перейти в директорию")
    print("  cd ..           - перейти в родительскую директорию")
    print("  mkdir <имя>     - создать директорию")
    print("  touch <имя>.<расш> - создать файл")
    print("  write <файл>    - добавить содержимое в txt файл")
    print("  read <файл>     - прочитать содержимое txt файла")
    print("  rm <имя>        - удалить файл/директорию")
    print("  pwd             - показать текущий путь")
    print("  tree            - показать всё дерево от корня")
    print("  help            - показать команды")
    print("  exit            - выход")
    print("*" * 50)


"""Интерактивный интерфейс для работы с файловой системой"""
print("*" * 50)
print("ФАЙЛОВАЯ СИСТЕМА v1.0")
print("*" * 50)
Menu()

# Создаем файловую систему с вводом даты для корня
fs = FileSystem()

while True:
    command = input(f"\n{fs.getCurrentPath()}> ").strip().split()

    if not command:
        continue

    cmd = command[0].lower()

    if cmd == "exit":
        print("До свидания!")
        break

    elif cmd == "help":
        Menu()

    elif cmd == "ls":
        fs.listContents()

    elif cmd == "pwd":
        print(fs.getCurrentPath())

    elif cmd == "tree":
        print("\nПолное дерево файловой системы:")
        fs._root.display()

    elif cmd == "cd":
        if len(command) < 2:
            print("Укажите папочку")
        else:
            fs.changeDirectory(command[1])

    elif cmd == "mkdir":
        if len(command) < 2:
            print("Укажите имя папочки")
        else:
            fs.createDirectory(command[1])

    elif cmd == "touch":
        if len(command) < 2:
            print("Укажите имя файла с расширением (например: document.txt)")
        else:
            filename = command[1]
            if "." in filename:
                name, ext = filename.rsplit(".", 1)
                fs.createFile(name, ext)
            else:
                print("Файл должен иметь расширение (например: document.txt)")

    elif cmd == "write":
        if len(command) < 2:
            print("Укажите имя файла")
        else:
            file_item = fs.findFile(command[1])
            if file_item and isinstance(file_item, File):
                file_item.addContent()
            else:
                print(f"Файл '{command[1]}' не найден")

    elif cmd == "read":
        if len(command) < 2:
            print("Укажите имя файла")
        else:
            file_item = fs.findFile(command[1])
            if file_item and isinstance(file_item, File):
                file_item.readContent()
            else:
                print(f"Файл '{command[1]}' не найден")

    elif cmd == "rm":
        if len(command) < 2:
            print("Укажите имя файла или директории")
        else:
            fs.deleteItem(command[1])

    else:
        print(f"Неизвестная команда: {cmd}")
