from datetime import datetime

class FileSystemItem:
    """Базовый интерфейс для файловой системы."""
    def __init__(self, name: str):
        self.name = name

    def get_size(self) -> int:
        raise NotImplementedError

    def display(self, indent=0):
        raise NotImplementedError


class File(FileSystemItem):
    """Файл с атрибутами размера, расширения и даты создания."""
    def __init__(self, name: str, size: int, extension: str):
        super().__init__(name)
        self.size = size
        self.extension = extension
        self.created_at = datetime.now()

    def get_size(self) -> int:
        return self.size

    def display(self, indent=0):
        print('  ' * indent + f"{self.name}.{self.extension} ({self.size} bytes)")


class Directory(FileSystemItem):
    """Директория, содержащая файлы и поддиректории."""
    def __init__(self, name: str):
        super().__init__(name)
        self.children = []

    def add(self, item: FileSystemItem):
        self.children.append(item)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)

    def display(self, indent=0):
        print('  ' * indent + f"[DIR] {self.name}/")
        for child in self.children:
            child.display(indent + 1)


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

    print("Структура файловой системы:")
    root.display()
    print(f"\nОбщий размер root: {root.get_size()} bytes")
    