import os
import shutil
from pathlib import Path

from nodes.block_markdown import extract_title
from nodes.block_markdown import markdown_to_html_node
from nodes.htmlnode import ParentNode

CWD = dir_path = os.path.dirname(os.path.realpath(__file__))
STATIC_PATH = "./static/"
PUBLIC_PATH = "./public/"
CONTENT_PATH = "./content/"
TEMPLATE_PATH = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(PUBLIC_PATH):
        shutil.rmtree(PUBLIC_PATH)

    print("Copying static assets to public directory...")
    copy_directories(STATIC_PATH, PUBLIC_PATH)

    print("Generating page...")
    generate_pages_recursive(
        CONTENT_PATH,
        TEMPLATE_PATH,
        PUBLIC_PATH,
    )


def copy_directories(source_path: str, dest_path: str) -> None:
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    for filename in os.listdir(source_path):
        from_path = os.path.join(source_path, filename)
        to_path = os.path.join(dest_path, filename)

        print(f" * {from_path} -> {to_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_directories(from_path, to_path)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node: ParentNode = markdown_to_html_node(markdown_content)
    try:
        html = node.to_html()
    except ValueError:
        raise

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


if __name__ == "__main__":
    main()

