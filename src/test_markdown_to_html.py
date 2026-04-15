import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    
    def test_paragraph(self):
        md = "This is a simple paragraph."
        node = markdown_to_html_node(md)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[0].children[0].value, "This is a simple paragraph.")

    def test_heading(self):
        md = "### This is a heading"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "h3")
        self.assertEqual(node.children[0].children[0].value, "This is a heading")

    def test_quote(self):
        md = "> This is a quote\n> with two lines"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "blockquote")
        # Ensure newlines are preserved and text is cleaned
        self.assertEqual(node.children[0].children[0].value, "This is a quote\nwith two lines")

    def test_code_block(self):
        md = "http://googleusercontent.com/immersive_entry_chip/0"

