import os
import tempfile
import unittest
from unittest.mock import patch

from src.mypackage.transforms.markdown_to_HTML import generate_page

class FakeMarkdownToHTMLNode:
    def __init__(self, markdown_content: str):
        self.markdown_content = markdown_content

    def get_title(self) -> str:

        if not self.markdown_content.strip():
            return ""
        return "Fake Title"

    def to_html(self) -> str:

        if not self.markdown_content.strip():
            return ""
        return "Fake HTML"

class TestMarkdownToHTML(unittest.TestCase):

    @patch("src.mypackage.transforms.markdown_to_HTML.MarkdownToHTMLNode", new = FakeMarkdownToHTMLNode)
    def test_generate_page_creates_dest_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            from_path = os.path.join(temp_dir, "input.md")
            template_path = os.path.join(temp_dir, "template.html")
            dest_dir = os.path.join(temp_dir, "nonexistent", "subdir")
            dest_path = os.path.join(dest_dir, "output.html")

            with open(from_path, "w", encoding="utf-8") as f:
                f.write("Some markdown content")

            with open(template_path, "w", encoding="utf-8") as f:
                f.write("Header {{ Title }} Footer {{ Content }}")

            generate_page(from_path, template_path, dest_path)

            self.assertTrue(os.path.exists(dest_path))
            with open(dest_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertEqual(content, "Header Fake Title Footer Fake HTML")

    @patch("src.mypackage.transforms.markdown_to_HTML.MarkdownToHTMLNode", new = FakeMarkdownToHTMLNode)
    def test_generate_page_with_empty_markdown(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            from_path = os.path.join(temp_dir, "empty.md")
            template_path = os.path.join(temp_dir, "template.html")
            dest_path = os.path.join(temp_dir, "output.html")

            with open(from_path, "w", encoding="utf-8") as f:
                f.write("")

            with open(template_path, "w", encoding="utf-8") as f:
                f.write("Header {{ Title }} Footer {{ Content }}")

            generate_page(from_path, template_path, dest_path)

            with open(dest_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertEqual(content, "Header  Footer ")

    @patch("src.mypackage.transforms.markdown_to_HTML.MarkdownToHTMLNode", new = FakeMarkdownToHTMLNode)
    def test_generate_page_template_without_placeholders(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            from_path = os.path.join(temp_dir, "nonempty.md")
            template_path = os.path.join(temp_dir, "template.html")
            dest_path = os.path.join(temp_dir, "output.html")

            with open(from_path, "w", encoding="utf-8") as f:
                f.write("Non-empty markdown content")

            with open(template_path, "w", encoding="utf-8") as f:
                f.write("Plain template without placeholders")

            generate_page(from_path, template_path, dest_path)

            with open(dest_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertEqual(content, "Plain template without placeholders")

if __name__ == '__main__':
    unittest.main()
