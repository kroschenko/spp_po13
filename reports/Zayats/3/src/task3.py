"""Модуль, реализующий файловую систему с паттернами Composite и Iterator."""
# pylint: disable=too-few-public-methods, duplicate-code
import random
from datetime import datetime


class FileSystemItem:
    """Базовый интерфейс для элементов файловой системы."""

    def __init__(self, name: str):
        """Инициализация элемента."""
        self.name = name

    def get_size(self) -> int:
        """Вернуть размер элемента."""
        raise NotImplementedError

    def display(self) -> None:
        """Отобразить элемент."""
        raise NotImplementedError

    def get_all_items(self) -> list:
        """Вернуть список всех элементов."""
        raise NotImplementedError


class File(FileSystemItem):
    """Файл с размером, расширением и датой создания."""

    def __init__(self, name: str, size: int, extension: str):
        """Создать файл."""
        super().__init__(name)
        self.size = size
        self.extension = extension
        self.created_at = datetime.now()

    def get_size(self) -> int:
        """Вернуть размер файла."""
        return self.size

    def display(self) -> None:
        """Отобразить файл."""
        print(
            f"File: {self.name}.{self.extension}, "
            f"Size: {self.size}, Created: {self.created_at}"
        )

    def get_all_items(self) -> list:
        """Вернуть список, содержащий только этот файл."""
        return [self]


class Directory(FileSystemItem):
    """Директория, содержащая файлы и поддиректории."""

    def __init__(self, name: str):
        """Создать директорию."""
        super().__init__(name)
        self.children: list[FileSystemItem] = []

    def add(self, fs_item: FileSystemItem) -> None:
        """Добавить элемент в директорию."""
        self.children.append(fs_item)

    def get_size(self) -> int:
        """Вернуть суммарный размер директории."""
        return sum(child.get_size() for child in self.children)

    def display(self) -> None:
        """Отобразить директорию."""
        print(f"Directory: {self.name}, Total size: {self.get_size()}")

    def get_all_items(self) -> list:
        """Рекурсивно вернуть все элементы директории."""
        all_items: list[FileSystemItem] = [self]
        for child in self.children:
            all_items.extend(child.get_all_items())
        return all_items


class RandomIterator:
    """Итератор, возвращающий элементы в случайном порядке."""

    def __init__(self, fs_root: FileSystemItem):
        """Инициализация итератора."""
        self.items = fs_root.get_all_items()
        random.shuffle(self.items)
        self.index = 0

    def __iter__(self):
        """Вернуть итератор."""
        return self

    def __next__(self) -> FileSystemItem:
        """Вернуть следующий элемент."""
        if self.index >= len(self.items):
            raise StopIteration
        current_element = self.items[self.index]
        self.index += 1
        return current_element


def build_sample_tree() -> Directory:
    """Создать пример файловой структуры."""
    root_dir = Directory("root")
    docs_dir = Directory("Documents")
    pics_dir = Directory("Pictures")

    file_resume = File("resume", 1200, "pdf")
    file_photo = File("photo", 3500, "jpg")
    file_notes = File("notes", 800, "txt")

    docs_dir.add(file_resume)
    docs_dir.add(file_notes)
    pics_dir.add(file_photo)

    root_dir.add(docs_dir)
    root_dir.add(pics_dir)

    return root_dir


def main() -> None:
    """Точка входа в программу."""
    root_dir = build_sample_tree()

    print("Вывод файловой системы в случайном порядке:\n")
    for fs_element in RandomIterator(root_dir):
        fs_element.display()


if __name__ == "__main__":
    main()
