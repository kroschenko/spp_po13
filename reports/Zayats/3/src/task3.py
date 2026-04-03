import random
from datetime import datetime

class FileSystemItem:
    """Базовый интерфейс для файловой системы."""
    def __init__(self, name: str):
        self.name = name

    def get_size(self) -> int:
        raise NotImplementedError

    def display(self):
        raise NotImplementedError

    def get_all_items(self):
        """Возвращает все элементы (для итератора)."""
        raise NotImplementedError


class File(FileSystemItem):
    """Файл с размером, расширением и датой создания."""
    def __init__(self, name: str, size: int, extension: str):
        super().__init__(name)
        self.size = size
        self.extension = extension
        self.created_at = datetime.now()

    def get_size(self) -> int:
        return self.size

    def display(self):
        print(f"File: {self.name}.{self.extension}, Size: {self.size}, Created: {self.created_at}")

    def get_all_items(self):
        return [self]


class Directory(FileSystemItem):
    """Директория, содержащая файлы и поддиректории."""
    def __init__(self, name: str):
        super().__init__(name)
        self.children = []

    def add(self, item: FileSystemItem):
        self.children.append(item)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)

    def display(self):
        print(f"Directory: {self.name}, Total size: {self.get_size()}")

    def get_all_items(self):
        """Возвращает все элементы внутри директории, рекурсивно."""
        items = [self]
        for child in self.children:
            items.extend(child.get_all_items())
        return items


class RandomIterator:
    """Итератор, который возвращает элементы в случайном порядке."""
    def __init__(self, fs_root: FileSystemItem):
        self.items = fs_root.get_all_items()
        random.shuffle(self.items)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.items):
            raise StopIteration
        item = self.items[self.index]
        self.index += 1
        return item


# Пример использования
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

    print("Вывод файловой системы в случайном порядке:\n")
    for item in RandomIterator(root):
        item.display()