import unittest
from cipher     import Vigenere  # або твоя назва модуля

class TestVigenereCipher(unittest.TestCase):
    def setUp(self):
        self.alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
        self.alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.key = "Key"
        self.vigenere = Vigenere(self.key, self.alphabet_lower, self.alphabet_upper)

    def test_encrypt_basic(self):
        plaintext = "HELLO"
        ciphertext = self.vigenere.encrypt(plaintext)
        self.assertEqual(ciphertext, "RIJVS")

    def test_decrypt_basic(self):
        ciphertext = "RIJVS"
        decrypted = self.vigenere.decrypt(ciphertext)
        self.assertEqual(decrypted, "HELLO")

    def test_encrypt_with_lowercase(self):
        plaintext = "hello"
        ciphertext = self.vigenere.encrypt(plaintext)
        self.assertEqual(ciphertext, "rijvs")

    def test_decrypt_with_lowercase(self):
        ciphertext = "rijvs"
        decrypted = self.vigenere.decrypt(ciphertext)
        self.assertEqual(decrypted, "hello")

    def test_encrypt_with_non_letters(self):
        plaintext = "hello, world!"
        ciphertext = self.vigenere.encrypt(plaintext)
        self.assertEqual(ciphertext, "rijvs, uyvjn!")

    def test_decrypt_with_non_letters(self):
        ciphertext = "rijvs, uyvjn!"
        decrypted = self.vigenere.decrypt(ciphertext)
        self.assertEqual(decrypted, "hello, world!")

    def test_invalid_key(self):
        with self.assertRaises(ValueError):
            Vigenere("KE_Y", self.alphabet_lower, self.alphabet_upper)

if __name__ == '__main__':
    unittest.main()