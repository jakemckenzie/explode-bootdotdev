from mypackage.utils.markdown_to_blocks import markdown_to_blocks
from mypackage.block_to_block_type import block_to_block_type, BlockType
from mypackage.text_to_text_nodes import text_to_textnodes
from mypackage.text_node import TextNode, TextType
from mypackage.html_node import HTMLNode
from mypackage.leaf_node import LeafNode
from mypackage.parent_node import ParentNode
from typing import List

class MarkdownToHTMLNode:
    def __init__(self, markdown: str) -> None:
        self.markdown: str = markdown
        self.children: List[HTMLNode] = markdown_to_html_children(markdown)

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

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(tag="span", value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="strong", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="em", value=text_node.text)
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

def text_to_children(text: str) -> List[HTMLNode]:
    text = text.replace("\n", " ")
    result: List[HTMLNode] = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        result.append(text_node_to_html_node(text_node))
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
            ParentNode(tag="li", children=text_to_children(line))
            for line in lines
        ],
    )

def markdown_to_html_ordered_list(markdown: str) -> HTMLNode:
    lines = [remove_ordered_list_prefix(line) for line in markdown.split("\n")]
    return ParentNode(
        tag="ol",
        children=[
            ParentNode(tag="li", children=text_to_children(line))
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
    children = []
    for line_group in lines_grouped_by_prefix(markdown):
        if line_group.startswith(">"):
            children.append(markdown_to_html_quote(line_group))
        else:
            for block in markdown_to_blocks(line_group):
                children.extend(markdown_to_html_children(block))
    return ParentNode(tag="blockquote", children=children)

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

def markdown_to_html_node(markdown: str) -> HTMLNode:
    children = markdown_to_html_children(markdown)
    return ParentNode(tag = "div", children=children)
