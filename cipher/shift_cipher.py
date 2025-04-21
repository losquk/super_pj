from cipher import Cipher

class Shift_cipher(Cipher):
    def __init__(self, key, alphabet_lower, alphabet_upper ):
        super().__init__(key)
        self.alphabet_lower = alphabet_lower
        self.alphabet_upper = alphabet_upper
        self.lower_dict, self.upper_dict = self.alphabet_to_dict()
    def _shift_text(self, text, shift_value):
        pass

    def alphabet_to_dict(self) -> tuple:
        """
        Робить з стрічок алфавітів алфавіт-словник
        """
        lower_dict = {char: idx for idx, char in enumerate(self.alphabet_lower)}
        upper_dict = {char: idx for idx, char in enumerate(self.alphabet_upper)}
        return lower_dict, upper_dict

    def encrypt(self, text):
        pass

    def decrypt(self, text):
        pass