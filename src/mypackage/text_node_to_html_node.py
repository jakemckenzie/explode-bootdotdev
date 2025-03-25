from src.mypackage.text_node import TextNode, TextType
from src.mypackage.leaf_node import LeafNode

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("link text node must have a URL, no cap🙅‍♂️")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("image text node must have a URL, no cap🙅‍♂️")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"🚧Unsupported TextType🚧: {text_node.text_type}")