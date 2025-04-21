from .shift_cipher import Shift_cipher


class Vigenere(Shift_cipher):
    def __init__(self, key, alphabet_lower, alphabet_upper):
        super().__init__(key, alphabet_lower, alphabet_upper)
        self._validate_key()
    def _validate_key(self):
        """Перевіряє, чи ключ містить тільки символи з алфавіту"""
        for letter in self._key:
            if letter not in self.lower_dict and letter not in self.upper_dict:
                raise ValueError("В ключі є символи, яких немає в алфавіті")

    def _process_key(self, operation):
        """Конвертує ключ у список зсувів"""
        shift_values = []
        sign = 1 if operation == "encrypt" else -1

        for letter in self._key:
            if letter in self.lower_dict:
                shift_values.append(sign * self.lower_dict[letter])
            elif letter in self.upper_dict:
                shift_values.append(sign * self.upper_dict[letter])
        return shift_values

    def _shift_text(self, text, shift_values):
        key_index = 0
        result = []
        shift_len = len(shift_values)
        text = text.strip()
        for letter in text:
            if letter in self.lower_dict:
                index = self.lower_dict[letter]
                new_index = (index + shift_values[key_index % shift_len]) % len(self.alphabet_lower)
                result.append(self.alphabet_lower[new_index])
                key_index += 1  # ключ зсувається тільки якщо літера шифрується
            elif letter in self.upper_dict:
                index = self.upper_dict[letter]
                new_index = (index + shift_values[key_index % shift_len]) % len(self.alphabet_upper)
                result.append(self.alphabet_upper[new_index])
                key_index += 1  # те саме для великих літер
            else:
                result.append(letter)  # пробіл, цифра, спецсимвол — додається як є

        return "".join(result)

    def encrypt(self, text):
        shift_values = self._process_key("encrypt")
        return self._shift_text(text, shift_values)

    def decrypt(self, text):
        shift_values = self._process_key("decrypt")
        return self._shift_text(text, shift_values)
if __name__ == "__main__":
    vigenere = Vigenere("key", "abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    print(vigenere.decrypt("kfanidq"))