import os
import shutil
from pathlib import Path

from block_markdown import markdown_to_html_node


def copy_directory_contents_wrapper(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    copy_directory_contents(source, dest)


def copy_directory_contents(source, dest):
    for item in os.listdir(source):
        item_src = os.path.join(source, item)
        item_dest = os.path.join(dest, item)

        if os.path.isfile(item_src):
            new_path = shutil.copy(item_src, item_dest)
            print(f"The new path is: {new_path}")

        else:
            os.mkdir(item_dest)
            copy_directory_contents(item_src, item_dest)


def extract_title(markdown):
    lines = list(map(lambda l: l.strip(), markdown.split("\n")))
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as md_file, open(template_path, "r") as template_file:
        markdown_text = md_file.read()
        template_text = template_file.read()
    try:
        html_node = markdown_to_html_node(markdown_text)       
        html_string = html_node.to_html()
    except ValueError as e:
        e.args = (*e.args, f"file_name={from_path}")
        raise e
    md_page_title = extract_title(markdown_text)

    to_replace = {"{{ Title }}": md_page_title, "{{ Content }}": html_string}

    for old, new in to_replace.items():
        template_text = template_text.replace(old, new)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as dest_file:
        dest_file.write(template_text)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
