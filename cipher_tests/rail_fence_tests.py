import unittest
from cipher import Rail_fence_cipher

class TestRailFenceCipher(unittest.TestCase):
    def setUp(self):
        self.key = 3
        self.size = 5
        self.message = "hello"
        self.cipher = Rail_fence_cipher(self.key, [], self.size)

    def test_encrypt_decrypt_cycle(self):
        encrypted = self.cipher.encrypt(self.message)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(decrypted, self.message)
    def test_encrypt_decrypt_manually(self):
        encrypted = self.cipher.encrypt(self.message)
        manually_encrypted = "lelho!"
        self.assertEqual(manually_encrypted, encrypted)
        manually_decrypted = self.cipher.decrypt(manually_encrypted)
        self.assertEqual(manually_decrypted, self.message)
    def test_perm_length_matches_text(self):
        self.assertEqual(len(self.cipher._perm), self.size)
    def test_generate_perm_manually(self):
        manually_perm = [2,1,3,0,4]
        perm = self.cipher.generate_perm(self.size)
        self.assertEqual(perm, manually_perm)
    def test_perm_is_permutation(self):
        perm = self.cipher._perm
        self.assertEqual(sorted(perm), list(range(self.size)))
    def test_generate_perm_structure(self):
        cipher = Rail_fence_cipher(2, [], 4)
        self.assertEqual(cipher._perm, [1, 3, 0, 2])

if __name__ == '__main__':
    unittest.main()
