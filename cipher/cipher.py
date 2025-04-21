from abc import ABC, abstractmethod
class Cipher(ABC):
    '''
    Абстрактний клас для шифрів
    '''
    def __init__(self, key):
        self._key = key
    @abstractmethod
    def encrypt(self, text):
        """
        Абстрактний метод для шифрування.
        Підклас має реалізувати цей метод.
        """
        pass
    @abstractmethod
    def decrypt(self, text):
        """
        Абстрактний метод для дешифрування.
        Підклас має реалізувати цей метод.
        """
        pass
