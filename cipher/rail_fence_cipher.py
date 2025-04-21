from .cipher import Cipher
class Rail_fence_cipher(Cipher):
    """
    Клас для шифру частоколу.
    Реалізує шифрування і дешифрування тексту.

    Атрибути:
        key - Ключ, який є координатами дірок у решітці.
        perm - Перестановка для оптимізації процесу шифрування.
    """
    def __init__(self, key, perm, size):
        super().__init__(key)
        if len(perm) == 0:
            self._perm = self.generate_perm(size)
        else:
            self._perm = perm
    """
    Генерує перестановку шляхом побудови частоколу такого виду:
        *         *
      *   *    *     *
    *       *          *
    На прикладі ключ\висота 3
    Параметри:
        size (int) - розмір частоколу
    Повертає:
        list: перестановку 
    """
    def generate_perm(self, size):
        height = self._key

        plain_text = '*' * size
        mat = [[' ' for i in range(size)] for j in range(height)]
        row = height - 1
        col = 0
        direction = -1
        for letter in plain_text:
            mat[row][col] = letter
            col += 1
            row += direction
            if row < 0:
                row = 1
                direction = 1
            elif row >= height:
                row = height - 2
                direction = -1
        perm = []
        for i in range(height):
            for j in range(size):
                if mat[i][j] != ' ':
                    perm.append((i * size + j) % size)

        return perm
    def encrypt(self, text):
        """
        Шифрує текст за допомогою шифру частоколу.

        Параметри:
            text (str): Текст для шифрування.

        Повертає:
            str: Зашифрований текст.
        """

        crypto_text = [''] * len(text)
        for i, p in enumerate(self._perm):
            crypto_text[i] = text[p]
        return ''.join(crypto_text)

    def decrypt(self, crypto_text):
        """
        Дешифрує текст за допомогою шифру частоколу.

        Параметри:
            crypto_text (str): Зашифрований текст.

        Повертає:
            str: Дешифрований текст.
        """
        plain_text = [''] * len(crypto_text)
        for i, p in enumerate(self._perm):
            plain_text[p] = crypto_text[i]
        return ''.join(plain_text)
