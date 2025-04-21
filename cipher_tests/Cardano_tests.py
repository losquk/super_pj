import unittest
from cipher import Cardano_cipher

class TestCardanoCipher(unittest.TestCase):
    def setUp(self):
        self.key = [[0,3], [1,2], [2,0], [3,1]]  # Для 4x4 матриці
        self.n = 16  # N = 2x2 = 4 символи
        self.text = "мамамиларамурано"
        self.cipher = Cardano_cipher(self.key, [], self.n)

    def test_encrypt_decrypt_cycle(self):
        encrypted = self.cipher.encrypt(self.text)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(decrypted, self.text)

    def test_generate_perm(self):
        perm = self.cipher.generate_perm()
        self.assertEqual(len(perm), 16)
        self.assertEqual(len(set(perm)), 16)  # Всі індекси унікальні

    def test_rotate_coordinates(self):
        rot_90 = self.cipher.rotate_coordinates(90)
        self.assertEqual(rot_90, [(3, 3), (2, 2), (0, 1), (1, 0)])

        rot_180 = self.cipher.rotate_coordinates(180)
        self.assertEqual(rot_180, [(3, 0), (2, 1), (1, 3), (0, 2)])

        rot_270 = self.cipher.rotate_coordinates(270)
        self.assertEqual(rot_270, [(0, 0), (1, 1), (3, 2), (2, 3)])
    def test_encrypt_decrypt_manually(self):
        encrypted = self.cipher.encrypt(self.text)
        manually_encrypted = "рмрмиаааммлнуаоа"
        self.assertEqual(manually_encrypted, encrypted)
        manually_decrypted = self.cipher.decrypt(manually_encrypted)
        self.assertEqual(manually_decrypted, self.text)
    def test_generate_perm_manually(self):
        manually_perm = [3, 6, 8, 13, 1, 4, 10, 15, 2, 7, 9, 12, 0, 5, 11, 14]
        perm = self.cipher.generate_perm()
        self.assertEqual(manually_perm, perm)
if __name__ == '__main__':
    unittest.main()
