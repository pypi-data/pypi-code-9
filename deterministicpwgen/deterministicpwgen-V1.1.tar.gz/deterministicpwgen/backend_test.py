import backend
import unittest

class TestSeededRandom(unittest.TestCase):

    def test_seeded_random(self):
        sr = backend.SeededRandom("unit test seeded random")
        self.assertEqual(sr.random_bytes(8), "\xf0\xec\xf8\x98q/f\x08")
        self.assertEqual(sr.random_bytes(8), "\x16\x03\xdfQ\x06\x17M>")
        self.assertEqual(sr.random_bytes(8), "a#U\xd4'\x07\xe1\x86")
        sr.close()

class TestGeneration(unittest.TestCase):

    def test_generation(self):
        self.assertEqual(backend.generate("test 1", 5, "abc123"), "a11a3")
        self.assertEqual(backend.generate("test 2", 5, "abc123"), "3c321")
        self.assertEqual(backend.generate("test 3", 5, "abc123"), "213b3")

class TestKeyStretch(unittest.TestCase):

    def test_key_stretch(self):
        self.assertEqual(backend.stretch_key("test 1")[:5], "\xa2\x89\x90\xdbQ")
        self.assertEqual(backend.stretch_key("test 2")[:5], "\x07\x88\xa4\xbbz")
        self.assertEqual(backend.stretch_key("test 3")[:5], "Q\xdb\xcb\x1e\x98")

if __name__ == "__main__":
    unittest.main()
