import unittest
from src.mypackage.nodes.text_node import TextNode, TextType
from src.mypackage.utils.split_delimiter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = TextNode("Alpha **Beta** Gamma **Delta** Epsilon", TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Alpha ", TextType.NORMAL),
            TextNode("Beta", TextType.BOLD),
            TextNode(" Gamma ", TextType.NORMAL),
            TextNode("Delta", TextType.BOLD),
            TextNode(" Epsilon", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises_exception(self):
        node = TextNode("This has an `unmatched delimiter", TextType.NORMAL)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("unmatched delimiter", str(context.exception))
    def test_delimiter_at_edges(self):
        node = TextNode("`code`", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_alternating_pattern_multiple_occurrences(self):
        node = TextNode("first`second`third`fourth`fifth", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("first", TextType.NORMAL),
            TextNode("second", TextType.CODE),
            TextNode("third", TextType.NORMAL),
            TextNode("fourth", TextType.CODE),
            TextNode("fifth", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
