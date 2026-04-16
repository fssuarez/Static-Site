import unittest
from markdown_to_html import markdown_to_html_node
from htmlnode import ParentNode
from textnode import TextNode, LeafNode
from textnode import TextType

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

    def test_markdown_to_html_node_is_parent(self):
        md = "# heading\n\nparagraph"
        node = markdown_to_html_node(md)
        self.assertTrue(isinstance(node, ParentNode))
        self.assertEqual(node.tag, "div")
    
    def test_render_heading(self):
        md = "# heading"
        node = markdown_to_html_node(md)
    # If this raises NotImplementedError, the bug is in create_heading_block
        self.assertEqual(node.to_html(), "<div><h1>heading</h1></div>")

    def test_render_code(self):
        md = "```\ncode block\n```"
        node = markdown_to_html_node(md)
        # If this fails, the bug is in create_code_block
        self.assertEqual(node.to_html(), "<div><pre><code>code block</code></pre></div>")

    def test_render_list(self):
        md = "- item 1\n- item 2"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><ul><li>item 1</li><li>item 2</li></ul></div>")
    
    def test_text_node_to_html_node_conversion(self):
    # Test a plain text node
        tnode = TextNode("just text", TextType.TEXT)
        hnode = TextNode.text_node_to_html_node(tnode)
    # This must be a LeafNode, not an HTMLnode
        self.assertTrue(isinstance(hnode, LeafNode))
    
    # Test a bold node
        tnode_bold = TextNode("bold text", TextType.BOLD)
        hnode_bold = TextNode.text_node_to_html_node(tnode_bold)
        self.assertTrue(isinstance(hnode_bold, LeafNode))

