from typing import List
import unittest
from src.mypackage.nodes.text_node import TextNode, TextType
from src.mypackage.utils.split_nodes_image_and_link import split_nodes, split_nodes_image, split_nodes_link

class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/zjjcJKZ.png)",
            TextType.NORMAL
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://example.com/zjjcJKZ.png")
        ]
        self.assertListEqual(result, expected)

        
    def test_split_multiple_images(self):
        text = ("Text before ![first](https://example.com/first.jpg) middle "
                "![second](https://example.com/second.jpg) end.")
        node = TextNode(text, TextType.NORMAL)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text before ", TextType.NORMAL),
            TextNode("first", TextType.IMAGE, "https://example.com/first.jpg"),
            TextNode(" middle ", TextType.NORMAL),
            TextNode("second", TextType.IMAGE, "https://example.com/second.jpg"),
            TextNode(" end.", TextType.NORMAL)
        ]
        self.assertListEqual(result, expected)

    def test_consecutive_images(self):
        text = "Start![first](https://example.com/first.jpg)![second](https://example.com/second.jpg)End"
        node = TextNode(text, TextType.NORMAL)
        result = split_nodes_image([node])
        expected = [
            TextNode("Start", TextType.NORMAL),
            TextNode("first", TextType.IMAGE, "https://example.com/first.jpg"),
            TextNode("second", TextType.IMAGE, "https://example.com/second.jpg"),
            TextNode("End", TextType.NORMAL)
        ]
        self.assertListEqual(expected, result)
        
    def test_no_images_returns_original(self):
        node = TextNode("No images here", TextType.NORMAL)
        result = split_nodes_image([node])
        self.assertListEqual(result, [node])

    def test_split_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.NORMAL
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertListEqual(result, expected)
        
    def test_split_multiple_links(self):
        text = ("Here is a link [first](https://example.com/first) and "
                "another [second](https://example.com/second) in text.")
        node = TextNode(text, TextType.NORMAL)
        result = split_nodes_link([node])
        expected = [
            TextNode("Here is a link ", TextType.NORMAL),
            TextNode("first", TextType.LINK, "https://example.com/first"),
            TextNode(" and another ", TextType.NORMAL),
            TextNode("second", TextType.LINK, "https://example.com/second"),
            TextNode(" in text.", TextType.NORMAL)
        ]
        self.assertListEqual(result, expected)
        
    def test_no_links_returns_original(self):
        node = TextNode("Just plain text.", TextType.NORMAL)
        result = split_nodes_link([node])
        self.assertListEqual(result, [node])
    
    def test_image_at_beginning(self):
        text = "![start](https://example.com/start.jpg) and some following text"
        node = TextNode(text, TextType.NORMAL)
        result = split_nodes_image([node])
        expected = [
            TextNode("start", TextType.IMAGE, "https://example.com/start.jpg"),
            TextNode(" and some following text", TextType.NORMAL)
        ]
        self.assertListEqual(expected, result)

    def test_image_at_end(self):
        text = "Some text before ![end](https://example.com/end.jpg)"
        node = TextNode(text, TextType.NORMAL)
        result = split_nodes_image([node])
        expected = [
            TextNode("Some text before ", TextType.NORMAL),
            TextNode("end", TextType.IMAGE, "https://example.com/end.jpg")
        ]
        self.assertListEqual(expected, result)

    def test_link_only_content(self):
        text = "[only link](https://example.com/only)"
        node = TextNode(text, TextType.NORMAL)
        result = split_nodes_link([node])
        expected = [
            TextNode("only link", TextType.LINK, "https://example.com/only")
        ]
        self.assertListEqual(expected, result)

    def test_link_trailing_punctuation(self):
        text = "[Click](https://example.com/click)!"
        node = TextNode(text, TextType.NORMAL)
        result = split_nodes_link([node])
        expected = [
            TextNode("Click", TextType.LINK, "https://example.com/click"),
            TextNode("!", TextType.NORMAL)
        ]
        self.assertListEqual(expected, result)
    def test_image_only_content(self):
        text = "![solo](https://example.com/solo.jpg)"
        node = TextNode(text, TextType.NORMAL)
        result = split_nodes_image([node])
        expected = [
            TextNode("solo", TextType.IMAGE, "https://example.com/solo.jpg")
        ]
        self.assertListEqual(expected, result)
    
    def test_mixed_content_separate(self):
        text = ("Here is an image ![img](https://example.com/image.jpg) and "
                "a link [link](https://example.com/link)")
        node = TextNode(text, TextType.NORMAL)
        
        image_result = split_nodes_image([node])
        for n in image_result:
            self.assertNotEqual(n.text_type, TextType.LINK, 
                "Image splitting should not produce LINK nodes")
        
        link_result = split_nodes_link([node])
        for n in link_result:
            self.assertNotEqual(n.text_type, TextType.IMAGE,
                "Link splitting should not produce IMAGE nodes")

    def test_order_independence(self):
        text = ("Text with image ![img](https://example.com/image.jpg) and "
                "link [link](https://example.com/link)")
        original_node = TextNode(text, TextType.NORMAL)
        
        intermediate1 = split_nodes_image([original_node])
        result_order1 = split_nodes_link(intermediate1)
        
        intermediate2 = split_nodes_link([original_node])
        result_order2 = split_nodes_image(intermediate2)
        
        image_count1 = 0
        link_count1 = 0
        for n in result_order1:
            if n.text_type == TextType.IMAGE:
                image_count1 += 1
            elif n.text_type == TextType.LINK:
                link_count1 += 1

        image_count2 = 0
        link_count2 = 0
        for n in result_order2:
            if n.text_type == TextType.IMAGE:
                image_count2 += 1
            elif n.text_type == TextType.LINK:
                link_count2 += 1
        
        self.assertEqual(image_count1, 1, "There should be exactly one IMAGE token")
        self.assertEqual(link_count1, 1, "There should be exactly one LINK token")
        self.assertEqual(image_count2, 1, "There should be exactly one IMAGE token")
        self.assertEqual(link_count2, 1, "There should be exactly one LINK token")
    
    def test_dummy_injection_independence(self):
        def dummy_extract(text: str) -> List[tuple]:
            pos = text.find("DUMMY")
            if pos == -1:
                return []
            return [("DUMMY", "dummy_meta")]
        
        def dummy_format(token_text: str, token_meta: str) -> str:
            return token_text
        
        text = "Start DUMMY middle DUMMY end"
        node = TextNode(text, TextType.NORMAL)
        
        result = split_nodes([node], dummy_extract, dummy_format, TextType.LINK)
        
        self.assertTrue(len(result) >= 2, "Result should contain at least two nodes after splitting")

        self.assertEqual(result[1].text, "DUMMY", "Token text should be 'DUMMY'")
        self.assertEqual(result[1].text_type, TextType.LINK, "Token type should be LINK")

if __name__ == "__main__":
    unittest.main()

    