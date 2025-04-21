from .shift_cipher import Shift_cipher
class Ceasar_cipher(Shift_cipher):
    """
    Клас для шифру Цезаря.
    Реалізує шифрування і дешифрування тексту з використанням координатної решітки.

    Атрибути:
        key - Ключ, який є координатами дірок у решітці.
       alphabet_lower, alphabet_upper - нижній і верхній регістр алфавіту, відповідно
    """
    def __init__(self, key, alphabet_lower, alphabet_upper):
        super().__init__(key, alphabet_lower, alphabet_upper)

    def _shift_text(self, text, shift_value):
        """
        Загальний метод для шифрування та дешифрування, що приймає текст та значення зміщення
        """
        lower_dict, upper_dict = self.alphabet_to_dict()
        new_text = []
        for letter in text:
            if letter in lower_dict:
                index = lower_dict[letter]
                new_letter = self.alphabet_lower[(index + shift_value) % len(self.alphabet_lower)]
            elif letter in upper_dict:
                index = [letter]
                new_letter = self.alphabet_upper[(index + shift_value) % len(self.alphabet_upper)]
            else:
                new_letter = letter
            new_text.append(new_letter)
        return "".join(new_text)
    def encrypt(self, text):
        """
        Шифрування тексту за допомогою шифру Цезаря
        """
        return self._shift_text(text, self._key)

    def decrypt(self, text):
        """
        Дешифрування тексту за допомогою шифру Цезаря
        """
        return self._shift_text(text, -self._key)