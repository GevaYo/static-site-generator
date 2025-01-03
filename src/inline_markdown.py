import re

from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
            continue
        curr_nodes = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                curr_nodes.append(TextNode(parts[i], TextType.NORMAL_TEXT))
            else:
                curr_nodes.append(TextNode(parts[i], text_type))
        new_nodes.extend(curr_nodes)
    return new_nodes

def extract_markdown_images(text):
    regex_image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex_image_pattern, text)
    

def extract_markdown_links(text):
    regex_links_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex_links_pattern, text)

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        curr_nodes = []
        original_text = node.text
        for image in images:
            image_alt, image_url = image
            parts = original_text.split(f"![{image_alt}]({image_url})",1)
            if parts[0] != "":
                curr_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT))
            curr_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            original_text = parts[1]
        if original_text != "":
            curr_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT))
        new_nodes.extend(curr_nodes)
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        curr_nodes = []
        original_text = node.text
        for link in links:
            link_anchor, link_url = link
            parts = original_text.split(f"[{link_anchor}]({link_url})",1)
            if parts[0] != "":
                curr_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT))
            curr_nodes.append(TextNode(link_anchor, TextType.LINK, link_url))
            original_text = parts[1]
        if original_text != "":
            curr_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT))
        new_nodes.extend(curr_nodes)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.NORMAL_TEXT)
    res_img = split_nodes_images([node])
    res_link = split_nodes_links(res_img)
    res_bold = split_nodes_delimiter(res_link, '**', TextType.BOLD_TEXT)
    res_italic =  split_nodes_delimiter(res_bold, '*', TextType.ITALIC_TEXT)
    res_code =  split_nodes_delimiter(res_italic, '`', TextType.CODE_TEXT)
    return res_code
