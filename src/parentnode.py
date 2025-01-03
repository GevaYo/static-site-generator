from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        result = ""
        if self.tag is None:
            raise ValueError("No tag")
        if self.children is None:
            raise ValueError("No Childrens")

        for child in self.children:
            result += child.to_html()
        return f"<{self.tag}>{result}</{self.tag}>"
