import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_value_only(self):
        node = LeafNode(None, "Testing for No TAG")
        self.assertEqual(node.to_html(), "Testing for No TAG")

    def test_to_html_without_value_raise_exception(self):
        with self.assertRaises(ValueError):
            node = LeafNode("div", None)
            node.to_html()
    
    def test_to_html(self):
        node = LeafNode("p","Testing it")
        self.assertEqual(node.to_html(),"<p>Testing it</p>")
            
