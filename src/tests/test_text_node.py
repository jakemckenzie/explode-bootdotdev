import unittest

from src.mypackage.text_node import TextNode, TextType
class TestTextNode(unittest.TestCase):
    def test_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_repr(self):
        node = TextNode("Example", TextType.ITALIC, "https://example.com")
        expected = "TextNode(Example, italic, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_link_node_equality(self):
        node1 = TextNode("Link", TextType.LINK, "https://example.com")
        node2 = TextNode("Link", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)
    
    def test_not_equal_different_url(self):
        node1 = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, "https://example.org")
        self.assertNotEqual(node1, node2)
    
    def test_mutation_affects_equality(self):
        node1 = TextNode("Same", TextType.BOLD)
        node2 = TextNode("Same", TextType.BOLD)
        self.assertEqual(node1, node2)
        node2.text = "Different"
        self.assertNotEqual(node1, node2)
    
    

if __name__ == "__main__":
    unittest.main()