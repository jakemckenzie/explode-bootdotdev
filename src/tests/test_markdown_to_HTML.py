import unittest
from src.mypackage.transforms.markdown_to_HTML import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_empty_markdown(self):
        with self.assertRaises(ValueError):
            markdown_to_html_node("")

    def test_invalid_list_prefix(self):
        md = "*Item without space"
        html_tree = markdown_to_html_node(md)
        
        self.assertEqual(html_tree.tag, "div")
        self.assertEqual(len(html_tree.children), 1)
        
        self.assertEqual(html_tree.children[0].tag, "p")

    def test_nested_quotes(self):
        md = "> Outer quote\n> > Nested quote"
        html_tree = markdown_to_html_node(md)
        html_output = html_tree.to_html()
        
        self.assertIn("<blockquote", html_output)
        
        expected_substrings = ["Outer quote", "Nested quote"]
        for substring in expected_substrings:
            self.assertIn(substring, html_output)

    def test_real_markdown(self):
        complex_md = (
            "# Heading 1\n\n"
            "This is a *sample* paragraph with **bold text** and `inline code`.\n\n"
            "- Unordered item 1\n"
            "- Unordered item 2\n\n"
            "1. Ordered item 1\n"
            "2. Ordered item 2\n\n"
            "> Outer quote starts here.\n"
            "> > Nested quote inside outer quote.\n\n"
            "```\n"
            "def hello():\n"
            "    print(\"Hello World\")\n"
            "```"
        )
        
        html_tree = markdown_to_html_node(complex_md)
        html_output = html_tree.to_html()
        
        expected_substrings = [
            "<h1>", "Heading 1", "</h1>",
            "<p>", "This is a", "sample", "paragraph", "bold text", "inline code", "</p>",
            "<ul>", "<li>", "Unordered item 1", "</li>", "Unordered item 2", "</li>", "</ul>",
            "<ol>", "<li>", "Ordered item 1", "</li>", "Ordered item 2", "</li>", "</ol>",
            "<blockquote>", "Outer quote starts here.", "Nested quote inside outer quote.", "</blockquote>",
            "<pre>", "<code>", "def hello():", "print(\"Hello World\")", "</code>", "</pre>"
        ]
        
        for substring in expected_substrings:
            with self.subTest(substring=substring):
                self.assertIn(substring, html_output)

if __name__ == "__main__":
    unittest.main()
