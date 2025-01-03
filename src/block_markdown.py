import re

from inline_markdown import text_to_textnodes
from parentnode import ParentNode
from textnode import text_node_to_html_node


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.strip().split("\n\n") if block.strip()]


def block_to_block_type(block):
    heading_regex = r"^#{1,6}\s"
    unordered_list_regex = r"^[-\*]\s"

    if re.match(heading_regex, block) is not None:
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"

    lines = block.split("\n")
    if all(map(lambda line: line.startswith(">"), lines)):
        return "quote"

    if all(map(lambda line: bool(re.match(unordered_list_regex, line)), lines)):
        return "unordered_list"

    if all(map(is_valid_ordered_list_line, lines, range(1, len(lines) + 1))):
        return "ordered_list"

    return "paragraph"


def is_valid_ordered_list_line(line, expected_number):
    ordered_list_regex = r"^(\d+)\.\s"
    match = re.match(ordered_list_regex, line)
    return bool(match) and int(match.group(1)) == expected_number


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)  # divide markdown to blocks
    children = []
    for block in markdown_blocks:  # Traversing the blocks and converting to HTML Nodes
        html_block = block_to_html(block)
        children.append(html_block)
    return ParentNode("div", children)


def block_to_html(block):  # returns an HTMLNode
    block_type = block_to_block_type(block)

    if block_type == "heading":
        return heading_to_html_node(block)
    if block_type == "paragraph":
        return paragraph_to_html_node(block)
    if block_type == "quote":
        return quote_to_html_node(block)
    if block_type == "unordered_list":
        return unordered_list_to_html_node(block)
    if block_type == "ordered_list":
        return ordered_list_to_html_node(block)
    if block_type == "code":
        return code_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_child_nodes(text):
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def heading_to_html_node(block):
    length = 0
    while block[length] == "#":
        length += 1
    children = text_to_child_nodes(block[length + 1 :])
    return ParentNode(f"h{length}", children)


def paragraph_to_html_node(block):
    paragraph = " ".join(block.split("\n"))
    children = text_to_child_nodes(paragraph)
    return ParentNode("p", children)
    
def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_child_nodes(content)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    items = block.split('\n')
    html_items = []

    for item in items:
        text = item[2:]
        children = text_to_child_nodes(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def ordered_list_to_html_node(block):
    items = block.split('\n')
    html_items = []

    for item in items:
        text = item[3:]
        children = text_to_child_nodes(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_child_nodes(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


