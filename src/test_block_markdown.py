import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_blocks(self):
        # The standard happy path
        md = "# Heading\n\nThis is a paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "This is a paragraph."])

    def test_multiple_newlines(self):
        # Users often hit Enter 3 or 4 times. This shouldn't create empty blocks.
        md = "# Heading\n\n\n\nThis is a paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "This is a paragraph."])

    def test_trailing_and_leading_whitespace(self):
        # Blocks should be stripped of whitespace on the edges
        md = "   # Heading   \n\n   This is a paragraph.   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "This is a paragraph."])

    def test_list_and_quote_blocks(self):
        # Ensuring multi-line blocks are kept as single strings
        md = """
> This is a quote
> that spans two lines

* Item 1
* Item 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "> This is a quote\n> that spans two lines",
                "* Item 1\n* Item 2"
            ]
        )

    def test_empty_input(self):
        # Corner case: What if the file is just empty space?
        md = "   \n\n  \n "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_heading_basic(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_invalid(self):
        # Missing the space after #
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_code_block(self):
        code = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_quote_block(self):
        quote = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        # Quote with some missing '>'
        bad_quote = "> Line 1\nLine 2\n> Line 3"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        ul = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED)
        # Missing space after '-'
        bad_ul = "-Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(bad_ul), BlockType.PARAGRAPH)

    def test_ordered_list_success(self):
        ol = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED)

    def test_ordered_list_broken_sequence(self):
        # Starts at 1 but skips a number
        ol = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(ol), BlockType.PARAGRAPH)
        
        # Starts at the wrong number
        ol2 = "2. First\n3. Second"
        self.assertEqual(block_to_block_type(ol2), BlockType.PARAGRAPH)

    def test_paragraph(self):
        text = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()