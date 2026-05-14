"""Модуль, реализующий файловую систему с использованием паттерна Composite."""
# pylint: disable=too-few-public-methods, duplicate-code
from datetime import datetime


class FileSystemItem:
    """Базовый интерфейс для файловой системы."""

    def __init__(self, name: str):
        """Инициализация элемента с именем."""
        self.name = name

    def get_size(self) -> int:
        """Вернуть размер элемента."""
        raise NotImplementedError

    def display(self, indent: int = 0):
        """Отобразить элемент с отступом."""
        raise NotImplementedError


class File(FileSystemItem):
    """Файл с атрибутами размера, расширения и даты создания."""

    def __init__(self, name: str, size: int, extension: str):
        """Создать файл."""
        super().__init__(name)
        self.size = size
        self.extension = extension
        self.created_at = datetime.now()

    def get_size(self) -> int:
        """Вернуть размер файла."""
        return self.size

    def display(self, indent: int = 0):
        """Отобразить файл."""
        print('  ' * indent + f"{self.name}.{self.extension} ({self.size} bytes)")


class Directory(FileSystemItem):
    """Директория, содержащая файлы и поддиректории."""

    def __init__(self, name: str):
        """Создать директорию."""
        super().__init__(name)
        self.children: list[FileSystemItem] = []

    def add(self, item: FileSystemItem):
        """Добавить элемент (файл или директорию)."""
        self.children.append(item)

    def get_size(self) -> int:
        """Вернуть суммарный размер директории."""
        return sum(child.get_size() for child in self.children)

    def display(self, indent: int = 0):
        """Отобразить структуру директории."""
        print('  ' * indent + f"[DIR] {self.name}/")
        for child in self.children:
            child.display(indent + 1)


if __name__ == "__main__":
    root = Directory("root")
    docs = Directory("Documents")
    pics = Directory("Pictures")

    file1 = File("resume", 1200, "pdf")
    file2 = File("photo", 3500, "jpg")
    file3 = File("notes", 800, "txt")

    docs.add(file1)
    docs.add(file3)
    pics.add(file2)
    root.add(docs)
    root.add(pics)

    print("Структура файловой системы:")
    root.display()
    print(f"\nОбщий размер root: {root.get_size()} bytes")
