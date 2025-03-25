from typing import List
from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter
from split_nodes_image_and_link import split_nodes_image, split_nodes_link

def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
