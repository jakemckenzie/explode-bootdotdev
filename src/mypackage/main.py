from src.mypackage.text_node import TextNode, TextType
from src.mypackage.html_node import HTMLNode
from src.mypackage.parent_node import ParentNode
from src.mypackage.tree_node import TreeNode
from src.mypackage.leaf_node import LeafNode
from src.mypackage.text_node_to_html_node import text_node_to_html_node


def main():
    print("=== Demonstrating each file in mypackage/ except utils ===\n")

    # 1) text_node.py
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print("TextNode:", text_node)

    # 2) html_node.py
    html_node = HTMLNode(tag="p", value="Hello, HTMLNode!", props={"class": "my-paragraph"})
    print("HTMLNode:", html_node)

    # 3) parent_node.py
    parent = ParentNode(tag="div", children=[html_node])
    print("ParentNode:", parent)

    # 4) tree_node.py
    tree = TreeNode(tag="ul", value="This is a tree node")
    print("TreeNode:", tree)

    # 5) leaf_node.py
    leaf = LeafNode(tag="li", value="I am a leaf node!")
    print("LeafNode:", leaf)

    # 6) text_node_to_html_node.py
    converted = text_node_to_html_node(text_node)
    print("Converted TextNode to HTMLNode:", converted)


if __name__ == '__main__':
    main()