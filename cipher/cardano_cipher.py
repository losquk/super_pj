from numpy.testing.print_coercion_tables import print_coercion_table

from cipher import Cipher
class Cardano_cipher(Cipher):
    """
    Клас для шифру Кардано.
    Реалізує шифрування і дешифрування тексту з використанням координатної решітки.

    Атрибути:
        key - Ключ, який є координатами дірок у решітці.
        n - Розмірність матриці.
        perm - Перестановка для оптимізації процесу шифрування.
    """

    def __init__(self, key, perm, n):
        """
        Ініціалізує об'єкт шифру Кардано.

        Параметри:
            key (list): Ключ у вигляді списку координат.
            perm (list): Перестановка (якщо не передано, генерується автоматично).
            n (int): Розмірність матриці.
        """
        super().__init__(key)
        self.n = int(n ** 0.5)

        if len(perm) == 0:
            self._perm = self.generate_perm()
        else:
            self._perm = perm

    def rotate_coordinates(self, angle):
        def rotate(i, j):
            if angle == 90:
                return j, self.n - 1 - i
            elif angle == 0:
                return i, j
            elif angle == 180:
                return self.n - 1 - i, self.n - 1 - j
            elif angle == 270:
                return self.n - 1 - j, i
            else:
                raise ValueError("Неправильний кут повороту. Використай 0, 90, 180 або 270 градусів.")
        return [rotate(i, j) for i, j in self._key]


    def generate_perm(self):
        """
        Генерує перестановку для шифру Кардано.
        Записує, як переставилися індекси зашифрованого тексту за допомогою обробки координат на різних кутах повороту.

        Повертає:
            list: Перестановка індексів для шифрування та дешифрування.
        """
        perm = []
        for angle in [0, 90, 180, 270]:
            rotated_key = self.rotate_coordinates(angle)
            rotated_key = sorted(rotated_key, key=lambda x: x[0])
            for i, j in rotated_key:
                if ((i * self.n + j) % self.n**2) not in perm:
                    perm.append((i * self.n + j) % self.n**2)
        print(perm)
        return perm


    def encrypt(self, text):
        """
        Шифрує текст за допомогою шифру Кардано.

        Параметри:
            text (str): Текст для шифрування.

        Повертає:
            str: Зашифрований текст.
        """

        crypto_text = [''] * len(text)
        for i, p in enumerate(self._perm):
            crypto_text[p] = text[i]
        return ''.join(crypto_text)

    def decrypt(self, crypto_text):
        """
        Дешифрує текст за допомогою шифру Кардано.

        Параметри:
            crypto_text (str): Зашифрований текст.

        Повертає:
            str: Дешифрований текст.
        """
        plain_text = [''] * len(crypto_text)
        for i, p in enumerate(self._perm):
            plain_text[i] = crypto_text[p]
        return ''.join(plain_text)
if __name__ == "__main__":
    ob = Cardano_cipher([[0,3], [1,2], [2,0], [3,1]], [], 32)

