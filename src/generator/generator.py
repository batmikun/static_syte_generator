import os
from pathlib import Path

from nodes.htmlnode import ParentNode
from nodes.markdown import BlockMarkdown


class Generator:
    def __init__(self):
        print("Generating page...")

    def generate_pages_recursive(self, dir_path_content, template_path, dest_dir_path):
        for filename in os.listdir(dir_path_content):
            from_path = os.path.join(dir_path_content, filename)
            dest_path = os.path.join(dest_dir_path, filename)
            if os.path.isfile(from_path):
                dest_path = Path(dest_path).with_suffix(".html")
                self.generate_page(from_path, template_path, dest_path)
            else:
                self.generate_pages_recursive(from_path, template_path, dest_path)

    def generate_page(self, from_path, template_path, dest_path):
        print(f" * {from_path} {template_path} -> {dest_path}")
        from_file = open(from_path, "r")
        markdown_content = from_file.read()
        from_file.close()

        template_file = open(template_path, "r")
        template = template_file.read()
        template_file.close()

        block_markdown = BlockMarkdown(markdown_content)
        node: ParentNode = block_markdown.markdown_to_html_node()
        try:
            html = node.to_html()
        except ValueError:
            raise

        title = block_markdown.title
        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", html)

        dest_dir_path = os.path.dirname(dest_path)
        if dest_dir_path != "":
            os.makedirs(dest_dir_path, exist_ok=True)
        to_file = open(dest_path, "w")
        to_file.write(template)

