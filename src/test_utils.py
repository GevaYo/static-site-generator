import unittest

from utils import extract_title


class TestUtils(unittest.TestCase):
    def test_extract_title(self):
        test = """ # Tolkien Fan Club

        **I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)
        """
        self.assertEqual(extract_title(test), "Tolkien Fan Club")

    def test_extract_title_exception(self):
        test = " ## some h2 here"
        with self.assertRaises(Exception):
            extract_title(test)
