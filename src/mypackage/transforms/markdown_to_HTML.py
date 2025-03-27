import os
from src.mypackage.transforms.markdown_to_blocks import markdown_to_blocks
from src.mypackage.transforms.block_to_block_type import block_to_block_type, BlockType
from src.mypackage.nodes.text_to_text_nodes import text_to_textnodes
from src.mypackage.nodes.text_node import TextNode, TextType
from src.mypackage.nodes.html_node import HTMLNode
from src.mypackage.nodes.leaf_node import LeafNode
from src.mypackage.nodes.parent_node import ParentNode
from typing import List

import sys
basepath = sys.argv[1] if len(sys.argv) > 1 else "/"


class HTMLNode:
    def __init__(self, tag: str, value: str = "", props: dict = None, children: List['HTMLNode'] = None):
        self.tag = tag
        self.value = value
        self.props = props or {}
        self.children = children or []

    def to_html(self) -> str:
        raise NotImplementedError

    def get_title(self) -> str:
        for child in self.children:
            if child.tag == "h1":
                if child.value:
                    return child.value.strip()
        raise ValueError("No h1 header found in markdown.")

    def to_html(self) -> str:
        content_children: List[HTMLNode] = []
        title_removed = False
        for child in self.children:
            if not title_removed and child.tag == "h1":
                title_removed = True
                continue
            content_children.append(child)
        container = HTMLNode(tag="div", children=content_children)
        return container.to_html()

def text_node_to_html_node(text_node: TextNode, wrap: bool = True) -> HTMLNode:
    if text_node.text_type == TextType.NORMAL:
        # If we don't want to wrap normal text, return a LeafNode with no tag
        if not wrap:
            return LeafNode(tag=None, value=text_node.text)
        return LeafNode(tag="span", value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        return LeafNode(tag="span", value=text_node.text)

def remove_unordered_list_prefix(line: str) -> str:
    if line and line[0] in ("*", "-") and len(line) > 1 and line[1] == " ":
        return line[2:]
    return line

def remove_ordered_list_prefix(line: str) -> str:
    pos = line.find(". ")
    if pos != -1 and line[:pos].isdigit():
        return line[pos+2:]
    return line

def remove_quote_prefix(line: str) -> str:
    if line.startswith(">"):
        return line[1:].lstrip()
    return line

def text_to_children(text: str, wrap: bool = True) -> List[HTMLNode]:
    text = text.replace("\n", " ")
    result: List[HTMLNode] = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        result.append(text_node_to_html_node(text_node, wrap=wrap))
    return result

def markdown_to_html_paragraph(markdown: str) -> HTMLNode:
    return ParentNode(tag="p", children=text_to_children(markdown))

def markdown_to_html_heading(markdown: str) -> HTMLNode:
    heading_level, text = markdown.split(" ", maxsplit=1)
    return LeafNode(tag=f"h{len(heading_level)}", value=text)

def markdown_to_html_code(markdown: str) -> HTMLNode:
    return ParentNode(
        tag="pre",
        children=[LeafNode(tag="code", value=markdown.strip("`").strip())],
    )

def markdown_to_html_unordered_list(markdown: str) -> HTMLNode:
    lines = [remove_unordered_list_prefix(line) for line in markdown.split("\n")]
    return ParentNode(
        tag="ul",
        children=[
            ParentNode(tag="li", children=text_to_children(line, wrap=False))
            for line in lines
        ],
    )

def markdown_to_html_ordered_list(markdown: str) -> HTMLNode:
    lines = [remove_ordered_list_prefix(line) for line in markdown.split("\n")]
    return ParentNode(
        tag="ol",
        children=[
            ParentNode(tag="li", children=text_to_children(line, wrap=False))
            for line in lines
        ],
    )

def lines_grouped_by_prefix(markdown: str) -> List[str]:
    result = []
    old_line_type = None
    for line in (remove_quote_prefix(line) for line in markdown.split("\n")):
        line_type = "QUOTE" if line != line.lstrip() else "NO_QUOTE"
        if line_type != old_line_type:
            result.append(line)
            old_line_type = line_type
        else:
            result[-1] += "\n" + line
    return result

def markdown_to_html_quote(markdown: str) -> HTMLNode:
    lines = [remove_quote_prefix(line) for line in markdown.split("\n")]
    quote_text = " ".join(lines).strip()
    quote_content = LeafNode(tag=None, value=quote_text)
    return ParentNode(tag="blockquote", children=[quote_content])


def markdown_to_html_children(markdown: str) -> List[HTMLNode]:
    blocks = markdown_to_blocks(markdown)
    children: List[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(markdown_to_html_paragraph(block))
        elif block_type == BlockType.HEADING:
            children.append(markdown_to_html_heading(block))
        elif block_type == BlockType.CODE:
            children.append(markdown_to_html_code(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(markdown_to_html_unordered_list(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(markdown_to_html_ordered_list(block))
        elif block_type == BlockType.QUOTE:
            children.append(markdown_to_html_quote(block))
    return children

def extract_title(markdown: str) -> str:    
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.strip("# ")
    raise Exception("No heading in markdown file")

def nodes_to_html(nodes: List[HTMLNode]) -> str:
    return ''.join(node.to_html() for node in nodes)

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content: str = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content: str = f.read()
    
    title: str = extract_title(markdown_content)
    html_nodes: List[HTMLNode] = markdown_to_html_children(markdown_content)
    html_content: str = nodes_to_html(html_nodes)
    final_html: str = template_content.replace("{{ BASEPATH }}", basepath).replace("{{ BASEPATH }}", basepath)
    dest_dir: str = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)