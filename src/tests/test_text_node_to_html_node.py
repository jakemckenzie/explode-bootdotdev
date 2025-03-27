import unittest
from src.mypackage.nodes.text_node import TextNode, TextType
from src.mypackage.nodes.text_node_to_html_node import text_node_to_html_node
from src.mypackage.nodes.leaf_node import LeafNode

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_normal_text(self) -> None:
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self) -> None:
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_text(self) -> None:
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code_text(self) -> None:
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")

    def test_link_text(self) -> None:
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image_text(self) -> None:
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Alt text"})

    def test_invalid_text_type(self) -> None:
        class FakeType:
            pass
        node = TextNode("Test", FakeType())
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
    def test_returns_leafnode_instance(self) -> None:
        node = TextNode("Instance test", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)

    def test_input_node_unchanged(self) -> None:
        original = TextNode("Do not change me", TextType.ITALIC, "https://dummy.url")
        orig_text = original.text
        orig_type = original.text_type
        orig_url = original.url
        _ = text_node_to_html_node(original)
        self.assertEqual(original.text, orig_text)
        self.assertEqual(original.text_type, orig_type)
        self.assertEqual(original.url, orig_url)

    def test_empty_text_value(self) -> None:
        node = TextNode("", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "")

if __name__ == "__main__":
    unittest.main()