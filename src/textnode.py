from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type.value == other.text_type.value
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    text_type = text_node.text_type

    if text_type == TextType.NORMAL_TEXT:
        return LeafNode(None, text_node.text)
    elif text_type == TextType.BOLD_TEXT:
        return LeafNode("b", text_node.text)
    elif text_type == TextType.ITALIC_TEXT:
        return LeafNode("i", text_node.text)
    elif text_type == TextType.CODE_TEXT:
        return LeafNode("code", text_node.text)
    elif text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    elif text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    else:
        raise Exception("Text type isn't compatible")

