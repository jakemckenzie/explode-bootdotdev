from typing import List, Callable
from src.mypackage.text_node import TextNode, TextType
from src.mypackage.utils.extract_links import extract_markdown_images, extract_markdown_links

def should_split(
    node: TextNode, 
    extract_func: Callable[[str], List[tuple]]
) -> bool:
    return (
        node.text_type == TextType.NORMAL and 
        bool(node.text) and 
        bool(extract_func(node.text
        )
    )
)

def split_node_once(
    node: TextNode,
    extract_func: Callable[[str], List[tuple]],
    format_func: Callable[[str, str], str],
    new_type: TextType
) -> List[TextNode]:
    tokens = extract_func(node.text)
    token = tokens[0]
    delimiter = format_func(*token)
    head, sep, tail = node.text.partition(delimiter)

    nodes: List[TextNode] = []
    if head:
        nodes.append(TextNode(head, TextType.NORMAL))

    nodes.append(TextNode(token[0], new_type, token[1]))
    if tail:
        nodes.append(TextNode(tail, TextType.NORMAL))
    return nodes

def recursive_split_node(
    node: TextNode,
    extract_func: Callable[[str], List[tuple]],
    format_func: Callable[[str, str], str],
    new_type: TextType
) -> List[TextNode]:
    if not should_split(node, extract_func):
        return [node]
    
    split_once = split_node_once(node, extract_func, format_func, new_type)
    result: List[TextNode] = []

    for subnode in split_once:
        if should_split(subnode, extract_func):
            result.extend(recursive_split_node(subnode, extract_func, format_func, new_type))
        else:
            result.append(subnode)
    return result


def split_nodes(
    nodes: List[TextNode],
    extract_func: Callable[[str], List[tuple]],
    format_func: Callable[[str, str], str],
    new_type: TextType
) -> List[TextNode]:
    result: List[TextNode] = []

    for node in nodes:
        result.extend(recursive_split_node(node, extract_func, format_func, new_type))
    return result

def split_nodes_image(nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes(
        nodes,
        extract_markdown_images,
        lambda alt, src: f"![{alt}]({src})",
        TextType.IMAGE
    )

def split_nodes_link(nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes(
        nodes,
        extract_markdown_links,
        lambda text, href: f"[{text}]({href})",
        TextType.LINK
    )
