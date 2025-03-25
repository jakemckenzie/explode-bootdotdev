from typing import List
from textnode import TextNode, TextType

def split_nodes_delimiter(
        old_nodes: List[TextNode], 
        delimiter: str, 
        new_type: TextType
    ) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL or delimiter not in node.text:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"🙅‍♂️Invalid markdown syntax: unmatched delimiter '{delimiter}' in text: {node.text}🙅‍♂️")

        parts = node.text.split(delimiter)
        # when you split a string by a delimiter, the resulting list alternates 
        # between segments outside the delimiter (even indices) and segments 
        # that were between the delimiters (odd indices)
        for idx, part in enumerate(parts):
            # always create a node (even empty strings) to preserve exact segmentation
            current_type = TextType.NORMAL if idx % 2 == 0 else new_type
            new_nodes.append(TextNode(part, current_type, node.url))
    return new_nodes
