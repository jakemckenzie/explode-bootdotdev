import unittest
from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self) -> None:
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self) -> None:
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_missing_tag_raises_error(self) -> None:
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child_node])

    def test_missing_children_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            ParentNode("div", [])
    
if __name__ == "__main__":
    unittest.main()
