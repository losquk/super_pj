import unittest

from fontTools.misc.eexec import encrypt

from cipher import Ceasar_cipher

class TestCeasarCipher(unittest.TestCase):
    def setUp(self):
        self.lower = "абвгґдеєжзийікї"
        self.upper = "АБВГҐДЕЄЖЗИЙІКЇ"
        self.key = 3
        self.message = "абвг!"
        self.cipher = Ceasar_cipher(self.key, self.lower, self.upper)
    def test_encrypt_decrypt_manually(self):
        encrypted = self.cipher.encrypt(self.message)
        manually_encrypted = "гґде!"
        self.assertEqual(manually_encrypted, encrypted)
        manually_decrypted = self.cipher.decrypt(manually_encrypted)
        self.assertEqual(manually_decrypted, self.message)
    def test_encrypt_decrypt(self):
        encrypted = self.cipher.encrypt(self.message)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(decrypted, self.message)

    def test_alphabet_to_dict(self):
        lower_dict, upper_dict = self.cipher.alphabet_to_dict()
        self.assertEqual(lower_dict["а"], 0)
        self.assertEqual(upper_dict["А"], 0)
        self.assertEqual(lower_dict[self.lower[-1]], len(self.lower) - 1)

    def test_non_alpha_characters(self):
        msg = "123!? АБВ"
        encrypted = self.cipher.encrypt(msg)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(decrypted, msg)

if __name__ == '__main__':
    unittest.main()
