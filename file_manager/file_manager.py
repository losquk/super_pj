from ast import literal_eval

from cipher import Ceasar_cipher, Rail_fence_cipher, Cardano_cipher, Vigenere
import os
class File_manager:
    """
    Клас для роботи з файлами.
    зчитує і розбиває файл на блоки, зчитує алфавіт.

    Атрибути:
        input_filename, output_filename - Вхідний і вихідний файл.
        block_size - Довжина блоку.
        alphabet_filename - Назва файлу алфавіту для шифру Цезаря.
    """
    def __init__(self, input_filename, block_size, output_filename, alphabet_filename):
        self.input_filename = input_filename
        if block_size == 0:
            self.block_size = os.path.getsize(input_filename)
        else:
            self.block_size = block_size
        self.output_filename = output_filename
        if alphabet_filename:
            self.alphabet_lower, self.alphabet_upper = self.read_alphabet(alphabet_filename)
        else:
            self.alphabet_lower, self.alphabet_upper = "", ""
        """
            Генератор, що зчитує файл по блокам 
        """
    def read_file_by_block(self):
        with open(self.input_filename, "rb") as file:
            while block := file.read(self.block_size):
                if len(block) < self.block_size:
                    block += b'\x20' * (self.block_size - len(block))
                yield block

    """
        Зчитує алфавіт
    """
    def read_alphabet(self, filename) -> tuple:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                alphabet = file.read().strip()
            if not alphabet:
                raise ValueError("Алфавіт у файлі порожній.")
            alphabet_set = sorted(set(alphabet))
            alphabet_lower = "".join(ch for ch in alphabet_set if ch.islower() or not ch.isalpha())
            alphabet_upper = "".join(ch for ch in alphabet_set if ch.isupper() or not ch.isalpha())
            return alphabet_lower, alphabet_upper
        except FileNotFoundError:
            print(f"Помилка: файл '{filename}' не знайдено.")
            return "", ""
        except ValueError as e:
            print(f"Помилка: {e}")
            return "", ""

    @staticmethod
    def load_cardano_key(filename: str) -> list[tuple[int, int]]:
        """
        Статичний метод для завантаження ключа Кардано з файлу.
        """
        key = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    key.append(tuple(literal_eval(line.strip())))
        return key
    """
        Шифрує/дешифрує файл по блоках і записує їх по блоках
        Приймає в себе ключ і тип шифру 
    """
    def file_encrypt(self, key, cipher_type):
        with open(self.output_filename, "wb") as output_file:

            if cipher_type == "ceasar":
                caesar_cipher = Ceasar_cipher(key, self.alphabet_lower, self.alphabet_upper)
                for block in self.read_file_by_block():
                    encrypted_block = caesar_cipher.encrypt(block.decode('utf-8', errors='ignore'))
                    output_file.write(encrypted_block.encode('utf-8'))
            elif cipher_type == "rail fence":
                rail_fence_cipher = Rail_fence_cipher(key, [], self.block_size)
                for block in self.read_file_by_block():
                    encrypted_block = rail_fence_cipher.encrypt(block.decode('utf-8', errors='ignore'))
                    output_file.write(encrypted_block.encode('utf-8'))
            elif cipher_type == "cardano":
                cardano_cipher = Cardano_cipher(key, [], self.block_size)
                for block in self.read_file_by_block():
                    encrypted_block = cardano_cipher.encrypt(block.decode('utf-8', errors='ignore'))
                    output_file.write(encrypted_block.encode('utf-8'))
            elif cipher_type == "vigenere":
                vigenere = Vigenere(key, self.alphabet_lower, self.alphabet_upper)
                for block in self.read_file_by_block():
                    encrypted_block = vigenere.encrypt(block.decode('utf-8', errors='ignore'))
                    output_file.write(encrypted_block.encode('utf-8'))
    def file_decrypt(self, key, cipher_type):
        with open(self.output_filename, "wb") as output_file:

            if cipher_type == "ceasar":
                caesar_cipher = Ceasar_cipher(key, self.alphabet_lower, self.alphabet_upper)
                for block in self.read_file_by_block():
                    decrypted_block = caesar_cipher.decrypt(block.decode('utf-8', errors='ignore'))
                    output_file.write(decrypted_block.encode('utf-8'))
            elif cipher_type == "rail_fence":
                rail_fence_cipher = Rail_fence_cipher(key, [], self.block_size)
                for block in self.read_file_by_block():
                    decrypted_block = rail_fence_cipher.decrypt(block.decode('utf-8', errors='ignore'))
                    output_file.write(decrypted_block.encode('utf-8'))
            elif cipher_type == "cardano":
                cardano_cipher = Cardano_cipher(key, [], self.block_size)
                for block in self.read_file_by_block():
                    decrypted_block = cardano_cipher.decrypt(block.decode('utf-8', errors='ignore'))
                    output_file.write(decrypted_block.encode('utf-8'))
            elif cipher_type == "vigenere":
                vigenere = Vigenere(key, self.alphabet_lower, self.alphabet_upper)
                for block in self.read_file_by_block():
                    decrypted_block = vigenere.decrypt(block.decode('utf-8', errors='ignore'))
                    output_file.write(decrypted_block.encode('utf-8'))