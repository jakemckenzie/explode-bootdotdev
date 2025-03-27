import unittest
from src.mypackage.nodes.html_node import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self) -> None:
        node = HTMLNode(tag="p", value="Hello World")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self) -> None:
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(tag="a", value="Google", props=props)
        result = node.props_to_html()
        self.assertTrue(result.startswith(" "))
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)

    def test_repr(self) -> None:
        child_node = HTMLNode(tag="span", value="child text")
        props = {"class": "highlight"}
        node = HTMLNode(tag="div", children=[child_node], props=props)
        rep = repr(node)
        self.assertIn("div", rep)
        self.assertIn("child text", rep)
        self.assertIn("highlight", rep)

    def test_eq_non_htmlnode(self) -> None:
        node = HTMLNode(tag="p", value="Hello")
        self.assertNotEqual(node, "Hello")

if __name__ == "__main__":
    unittest.main()