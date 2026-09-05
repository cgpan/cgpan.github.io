import tempfile
import unittest
from pathlib import Path

from minigpt.tokenizer import CharTokenizer

TEXT = "To be, or not to be.\n"


class TokenizerTests(unittest.TestCase):
    def setUp(self):
        self.tok = CharTokenizer.from_text(TEXT)

    def test_roundtrip_is_lossless(self):
        self.assertEqual(self.tok.decode(self.tok.encode(TEXT)), TEXT)

    def test_vocab_size_matches_unique_chars(self):
        self.assertEqual(self.tok.vocab_size, len(set(TEXT)))

    def test_ids_are_in_range(self):
        ids = self.tok.encode(TEXT)
        self.assertTrue(all(0 <= i < self.tok.vocab_size for i in ids))

    def test_unknown_character_raises(self):
        with self.assertRaises(ValueError):
            CharTokenizer.from_text("abc").encode("z")

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "vocab.json"
            self.tok.save(path)
            self.assertEqual(CharTokenizer.load(path).encode(TEXT), self.tok.encode(TEXT))


if __name__ == "__main__":
    unittest.main()
