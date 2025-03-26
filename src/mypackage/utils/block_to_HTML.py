from typing import List
from mypackage import text_node_to_html_node
from mypackage.block_to_block_type import BlockType, block_to_block_type
from mypackage.html_node import HTMLNode
from mypackage.text_node import TextNode, TextType
from mypackage.utils import markdown_to_blocks, text_to_children

def process_heading_block(block: str) -> HTMLNode:
    level:int = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

    content = block[level + 1:].strip()
    children: List[str] = text_to_children(content)

    return HTMLNode(f"h{level}", children=children)

def process_code_block(block: str) -> HTMLNode:
    content = block[3:-3].strip()
    return text_node_to_html_node(TextNode(content, TextType.CODE))

def process_quote_block(block: str) -> HTMLNode:
    processed_lines: List[str] = []
    for line in block.split("\n"):
        if line.startswith(">"):
            processed_lines.append(line[1:].strip())
        else:
            processed_lines.append(line)

    content = "\n".join(processed_lines)
    children: List[HTMLNode] = text_to_children(content)
    return HTMLNode("blockquote", children = children)

def process_unordered_list_block(block: str) -> HTMLNode:
    items: List[HTMLNode]  = []  
    for line in block.split("\n"):
        if line.startswith("- "):
            item_text = line[2:].strip()
            item_children: List[HTMLNode] = text_to_children(item_text)
            items.append(HTMLNode("li", children = item_children))
    return HTMLNode("ul", children=items)

def process_ordered_list_block(block: str) -> HTMLNode:
    items: List[HTMLNode] = []
    for line in block.split("\n"):
        pos = line.find(". ")
        if pos != -1:
            item_text = line[pos + 2:].strip()
            item_children: List[HTMLNode] = text_to_children(item_text)
            items.append(HTMLNode("li", children = item_children))
    return HTMLNode("ol", children=items)

def process_paragraph_block(block: str) -> HTMLNode:
    children: List[str] = text_to_children(block)
    return HTMLNode("p", children=children)

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks: List[str] = markdown_to_blocks(markdown)
    html_block_nodes = []
    

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            node = process_heading_block(block)
        elif block_type == BlockType.CODE:
            node = process_code_block(block)
        elif block_type == BlockType.QUOTE:
            node = process_quote_block(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = process_unordered_list_block(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = process_ordered_list_block(block)
        else:
            node = process_paragraph_block(block)

        html_block_nodes.append(node)
    
    parent_node = HTMLNode("div", children = html_block_nodes)
    return parent_node