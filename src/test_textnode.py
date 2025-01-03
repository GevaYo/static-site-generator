import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node.url, None)

    def test_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node.text_type, node2.text_type)

    def test_text_to_html(self):
        converted = text_node_to_html_node(
            TextNode("Bold text", TextType.BOLD_TEXT)
        ).to_html()
        self.assertEqual(converted, "<b>Bold text</b>")


if __name__ == "__main__":
    unittest.main()
