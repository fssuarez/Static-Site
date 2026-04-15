import unittest
from textnode import TextNode, TextType
from inline_markdown import (split_nodes_delimiter, extract_markdown_images,
                              extract_markdown_links, split_nodes_image, split_nodes_link,
                              text_to_textnodes
                            )

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and section", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and section", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_exception_unclosed(self):
        node = TextNode("This is text with an **unclosed bold", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zcew34n.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zcew34n.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "Text with ![img1](url1) and ![img2](url2)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("img1", "url1"), ("img2", "url2")],
            matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com) and [another](https://www.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.boot.dev"),
            ],
            matches,
        )

    def test_extract_links_excludes_images(self):
        # This is the "Boss Level" test for your negative lookbehind!
        text = "This text has a [link](url1) but also an ![image](url2)"
        matches = extract_markdown_links(text)
        # It should ONLY find the link, not the image
        self.assertListEqual([("link", "url1")], matches)

    def test_extract_no_matches(self):
        text = "This text has no links or images."
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zcew34n.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zcew34n.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Check [Google](https://google.com) or [Boot.dev](https://boot.dev)!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" or ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_start(self):
        node = TextNode("[Start](url) with a link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start", TextType.LINK, "url"),
                TextNode(" with a link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_links_ignore_images(self):
        node = TextNode(
            "Here is a [link](url1) and an ![image](url2)",
            TextType.TEXT,
        )
        # This tests that your split_nodes_link uses the negative lookbehind
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url1"),
                TextNode(" and an ![image](url2)", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_text_to_textnodes_full(self):
        # Testing a string with all markdown types supported
        text = "This is **bold** text with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_text(self):
        # Testing plain text with no markdown
        text = "Just a plain old sentence."
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("Just a plain old sentence.", TextType.TEXT)], nodes)

    def test_text_to_textnodes_bold_italic_overlap(self):
        # Testing that bold is handled before italic correctly
        text = "This is **bold** and *italic*"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            nodes
        )

    def test_text_to_textnodes_no_text_between(self):
        # Testing elements right next to each other
        text = "**Bold***Italic*`code`"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Bold", TextType.BOLD),
                TextNode("Italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ],
            nodes
        )


if __name__ == "__main__":
    unittest.main()