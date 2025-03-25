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
    
    def test_mixed_children(self) -> None:
        child1 = LeafNode(None, "Raw text")
        child2 = LeafNode("b", "Bold")
        parent = ParentNode("p", [child1, child2])
        self.assertEqual(parent.to_html(), "<p>Raw text<b>Bold</b></p>")

    def test_multiple_children_order(self) -> None:
        children = [
            LeafNode("i", "First"),
            LeafNode("i", "Second"),
            LeafNode("i", "Third")
        ]
        parent = ParentNode("div", children)
        self.assertEqual(parent.to_html(), "<div><i>First</i><i>Second</i><i>Third</i></div>")

    def test_props_in_parent(self) -> None:
        child = LeafNode("span", "Child")
        parent = ParentNode("section", [child], props={"class": "container", "id": "main"})
        output = parent.to_html()
        self.assertTrue(output.startswith('<section class="container" id="main">'))
        self.assertTrue(output.endswith("</section>"))

    def test_nested_parent_nodes(self) -> None:
        grandchild = LeafNode("b", "Deep text")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span><b>Deep text</b></span></div>")

    def test_deep_recursion_multiple_levels(self) -> None:
        level3 = ParentNode("u", [LeafNode(None, "Underlined text")])
        level2 = ParentNode("i", [level3])
        level1 = ParentNode("p", [level2])
        self.assertEqual(
            level1.to_html(),
            "<p><i><u>Underlined text</u></i></p>"
        )
    
if __name__ == "__main__":
    unittest.main()
