import re
from enum import Enum

from nodes.htmlnode import LeafNode
from nodes.htmlnode import ParentNode
from nodes.textnode import TextNode
from nodes.textnode import TextType


class Markdown:
    pass


class BlockType(Enum):
    PARAGRPAH = 1
    HEADING = 2
    CODE = 3
    OLIST = 4
    ULIST = 5
    QUOTE = 6


class BlockMarkdown(Markdown):
    def __init__(self, markdown: str):
        self.content = markdown
        self.blocks = self.__markdown_to_blocks(markdown)
        self.title = self.__extract_title()

    def markdown_to_html_node(self) -> ParentNode:
        children = []
        for block in self.blocks:
            html_node = self.__block_to_html_node(block)
            children.append(html_node)
        return ParentNode("div", children, None)

    def __markdown_to_blocks(self, markdown: str) -> list[str]:
        blocks = markdown.split("\n\n")
        filtered_blocks = []
        for block in blocks:
            if block == "":
                continue
            block = block.strip()
            filtered_blocks.append(block)
        return filtered_blocks

    def __block_to_html_node(self, block: str) -> ParentNode:
        block_type = self.__block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRPAH:
                return self.__paragraph_to_html_node(block)
            case BlockType.HEADING:
                return self.__heading_to_html_node(block)
            case BlockType.CODE:
                return self.__code_to_html_node(block)
            case BlockType.OLIST:
                return self.__olist_to_html_node(block)
            case BlockType.ULIST:
                return self.__ulist_to_html_node(block)
            case BlockType.QUOTE:
                return self.__quote_to_html_node(block)
        raise ValueError("Invalid block type")

    def __block_to_block_type(self, block: str) -> BlockType:
        lines = block.split("\n")

        if (
            len(lines) > 1
            and lines[0].startswith("```")
            and lines[-1].startswith("```")
        ):
            return BlockType.CODE

        match block:
            case s if s.startswith("# "):
                return BlockType.HEADING
            case s if s.startswith("## "):
                return BlockType.HEADING
            case s if s.startswith("### "):
                return BlockType.HEADING
            case s if s.startswith("#### "):
                return BlockType.HEADING
            case s if s.startswith("##### "):
                return BlockType.HEADING
            case s if s.startswith("###### "):
                return BlockType.HEADING
            case s if s.startswith(">"):
                for line in lines:
                    if not line.startswith(">"):
                        return BlockType.PARAGRPAH
                return BlockType.QUOTE
            case s if s.startswith("* "):
                for line in lines:
                    if not line.startswith("* "):
                        return BlockType.PARAGRPAH
                return BlockType.ULIST
            case s if s.startswith("- "):
                for line in lines:
                    if not line.startswith("- "):
                        return BlockType.PARAGRPAH
                return BlockType.ULIST
            case s if s.startswith("1. "):
                i = 1
                for line in lines:
                    if not line.startswith(f"{i}. "):
                        return BlockType.PARAGRPAH
                    i += 1
                return BlockType.OLIST
            case _:
                return BlockType.PARAGRPAH

    def text_to_children(self, text: str) -> list[LeafNode]:
        text_nodes = InlineMarkdown(text).text_to_textnodes()
        children = []
        for text_node in text_nodes:
            html_node = TextNode.text_node_to_html_node(text_node)
            children.append(html_node)
        return children

    def __paragraph_to_html_node(self, block: str) -> ParentNode:
        lines = block.split("\n")
        paragraph = " ".join(lines)
        children = self.text_to_children(paragraph)
        return ParentNode("p", children)

    def __heading_to_html_node(self, block: str) -> ParentNode:
        level = 0
        for char in block:
            if char == "#":
                level += 1
            else:
                break
        if level + 1 >= len(block):
            raise ValueError(f"Invalid heading level: {level}")
        text = block[level + 1 :]
        children = self.text_to_children(text)
        return ParentNode(f"h{level}", children)

    def __code_to_html_node(self, block: str) -> ParentNode:
        if not block.startswith("```") or not block.endswith("```"):
            raise ValueError("Invalid code block")
        text = block[4:-3]
        children = self.text_to_children(text)
        code = ParentNode("code", children)
        return ParentNode("pre", [code])

    def __olist_to_html_node(self, block: str) -> ParentNode:
        items = block.split("\n")
        html_items = []
        for item in items:
            text = item[3:]
            children = self.text_to_children(text)
            html_items.append(ParentNode("li", children))
        return ParentNode("ol", html_items)

    def __ulist_to_html_node(self, block: str) -> ParentNode:
        items = block.split("\n")
        html_items = []
        for item in items:
            text = item[2:]
            children = self.text_to_children(text)
            html_items.append(ParentNode("li", children))
        return ParentNode("ul", html_items)

    def __quote_to_html_node(self, block: str) -> ParentNode:
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            if not line.startswith(">"):
                raise ValueError("Invalid quote block")
            new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = self.text_to_children(content)
        return ParentNode("blockquote", children)

    def __extract_title(self) -> str:
        lines = self.content.split("\n")
        for line in lines:
            if line.startswith("# "):
                return line[2:]
        raise ValueError("No title found")


class InlineMarkdown(Markdown):
    def __init__(self, text: str) -> None:
        self.text = text

    def text_to_textnodes(self) -> list[TextNode]:
        nodes = [TextNode(self.text, TextType.TEXT)]
        nodes = self.__split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = self.__split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        nodes = self.__split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = self.__split_nodes_image(nodes)
        nodes = self.__split_nodes_link(nodes)
        return nodes

    def __split_nodes_delimiter(
        self, old_nodes: list[TextNode], delimiter: str, text_type: TextType
    ) -> list[TextNode]:
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != text_type.TEXT:
                new_nodes.append(old_node)
                continue
            split_nodes = []
            sections = old_node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("Invalid markdown, bold section not closed")
            for i in range(len(sections)):
                if sections[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i], text_type.TEXT))
                else:
                    split_nodes.append(TextNode(sections[i], text_type.TEXT))
            new_nodes.extend(split_nodes)
        return new_nodes

    def __split_nodes_image(self, old_nodes: list[TextNode]) -> list[TextNode]:
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            original_text = old_node.text
            images = self.__extract_markdown_images(original_text)
            if len(images) == 0:
                new_nodes.append(old_node)
                continue
            for image in images:
                sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
                if len(sections) != 2:
                    raise ValueError("Invalid markdown, image section not closed")
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(
                    TextNode(
                        image[0],
                        TextType.IMAGE,
                        image[1],
                    )
                )
                original_text = sections[1]
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.TEXT))
        return new_nodes

    def __split_nodes_link(self, old_nodes: list[TextNode]) -> list[TextNode]:
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            original_text = old_node.text
            links = self.__extract_markdown_links(original_text)
            if len(links) == 0:
                new_nodes.append(old_node)
                continue
            for link in links:
                sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
                if len(sections) != 2:
                    raise ValueError("Invalid markdown, link section not closed")
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                original_text = sections[1]
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.TEXT))
        return new_nodes

    def __extract_markdown_images(self, text: str) -> list[str]:
        pattern = r"!\[(.*?)\]\((.*?)\)"
        matches = re.findall(pattern, text)
        return matches

    def __extract_markdown_links(self, text: str) -> list[str]:
        pattern = r"\[(.*?)\]\((.*?)\)"
        matches = re.findall(pattern, text)
        return matches

