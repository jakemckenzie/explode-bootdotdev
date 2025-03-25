import unittest
from extract_links import extract_markdown_images, extract_markdown_links

class TestExtractLinks(unittest.TestCase):
    def test_empty_matches(self):
        text = "There is no markdown here!"
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(expected, extract_markdown_images(text))
    
    def test_extract_multiple_images(self):
        text = ("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
                "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                    ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(expected, extract_markdown_images(text))
    
    def test_extract_markdown_links(self):
        text = ("This is text with a link [to boot dev](https://www.boot.dev) "
                "and [to youtube](https://www.youtube.com/@bootdotdev)")
        expected = [("to boot dev", "https://www.boot.dev"),
                    ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected, extract_markdown_links(text))
    
    def test_no_false_positives_for_images_in_links(self):
        text = ("This is an image: ![alt](https://example.com/img.png) "
                "and a link: [example](https://example.com)")
        expected_links = [("example", "https://example.com")]
        self.assertListEqual(expected_links, extract_markdown_links(text))

if __name__ == "__main__":
    unittest.main()
