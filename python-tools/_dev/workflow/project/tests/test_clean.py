import unittest

from minigpt.clean import clean_text, describe


class CleanTests(unittest.TestCase):
    def test_cleaning_twice_changes_nothing(self):
        raw = "To be,  or not to be.\r\n\r\n\r\nThat is the question.  \n"
        once = clean_text(raw)
        self.assertEqual(clean_text(once), once)

    def test_smart_quotes_and_spaces_are_normalised(self):
        self.assertEqual(clean_text("“Hi”   there"), '"Hi" there\n')

    def test_describe_counts(self):
        info = describe("aab\n")
        self.assertEqual(info["n_chars"], 4)
        self.assertEqual(info["vocab_size"], 3)
        self.assertEqual(info["most_common"][0], ("a", 2))


if __name__ == "__main__":
    unittest.main()
