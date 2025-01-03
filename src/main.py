import os
from utils import copy_directory_contents_wrapper, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    try:
        copy_directory_contents_wrapper(dir_path_static, dir_path_public)
        generate_pages_recursive(dir_path_content, template_path, dir_path_public)
        
    except Exception as e:
        print(e)


main()
