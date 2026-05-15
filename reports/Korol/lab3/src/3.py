class EncryptStrategy:
    def encrypt(self, text):
        raise NotImplementedError


class RemoveVowels(EncryptStrategy):
    def encrypt(self, text):
        vowels = "aeiouAEIOUаеёиоуыэюяАЕЁИОУЫЭЮЯ"

        return "".join(char for char in text if char not in vowels)


class CaesarCipher(EncryptStrategy):
    def __init__(self, shift):
        self.shift = shift

    def encrypt(self, text):
        result = ""

        for char in text:
            result += chr(ord(char) + self.shift)

        return result


class Encryptor:
    def __init__(self, strategy):
        self.strategy = strategy

    def encrypt(self, text):
        return self.strategy.encrypt(text)


file_name = input("Введите имя txt файла: ")

with open(file_name, "r", encoding="utf-8") as file:
    text = file.read()

print("1 - Удалить гласные")
print("2 - Шифр Цезаря")

choice = input("Выберите метод: ")

if choice == "1":
    encryptor = Encryptor(RemoveVowels())

    result = encryptor.encrypt(text)

    with open("without_vowels.txt", "w", encoding="utf-8") as file:
        file.write(result)

    print("Файл сохранен: without_vowels.txt")

elif choice == "2":
    shift = int(input("Введите сдвиг: "))

    encryptor = Encryptor(CaesarCipher(shift))

    result = encryptor.encrypt(text)

    with open("caesar_encrypted.txt", "w", encoding="utf-8") as file:
        file.write(result)

    print("Файл сохранен: caesar_encrypted.txt")

else:
    print("Неверный выбор")
