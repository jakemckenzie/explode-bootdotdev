import unittest
from src.mypackage.leaf_node import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_paragraph(self) -> None:
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self) -> None:
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_no_tag_returns_raw_text(self) -> None:
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_without_value_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leaf_with_props_in_output(self) -> None:
        node = LeafNode("span", "Some text", {"class": "highlight", "id": "main"})
        html_output = node.to_html()
        self.assertTrue(html_output.startswith("<span"))
        self.assertTrue(html_output.endswith("</span>"))
        self.assertIn('class="highlight"', html_output)
        self.assertIn('id="main"', html_output)

if __name__ == "__main__":
    unittest.main()
