import unittest
import os
from file_manager import File_manager

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.test_alphabet = "абвгґдеєжзийклмнопрстуфхцчшщьюяАБВГҐДЕЄЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
        self.alphabet_file = "alphabet.txt"
        with open(self.alphabet_file, "w", encoding="utf-8") as f:
            f.write(self.test_alphabet)

    def tearDown(self):
        os.remove(self.alphabet_file)
    def test_read_alphabet(self):
        fm = File_manager("test.txt", 1, "out.txt", self.alphabet_file)
        self.assertIn("а", fm.alphabet_lower)
        self.assertIn("Я", fm.alphabet_upper)

    def test_load_cardano_key(self):
        key_file = "key.txt"
        with open(key_file, "w", encoding="utf-8") as f:
            f.write("(0, 0)\n(1, 2)\n")
        key = File_manager.load_cardano_key(key_file)
        self.assertEqual(key, [(0, 0), (1, 2)])
        os.remove(key_file)

    def test_read_file_by_block(self):
        filename = "test_block.txt"
        with open(filename, "wb") as f:
            f.write("Привіт".encode("utf-8"))
        fm = File_manager(filename, 3, "out.txt", None)
        blocks = list(fm.read_file_by_block())
        self.assertTrue(all(isinstance(b, bytes) for b in blocks))
        os.remove(filename)

if __name__ == "__main__":
    unittest.main()
