import unittest

from htmlnode import HTMLnode, LeafNode, ParentNode


class TestHTMLnode(unittest.TestCase):
    def test_eq(self):
        node = HTMLnode("h1", "This is a test")
        node2 = HTMLnode("p", "This is a test")
        self.assertNotEqual(node, node2)
        node3 = HTMLnode("p", "This is a test")
        node4 = HTMLnode("p", "This is a test")
        self.assertEqual(node3, node4)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("a", "This is a test!")
        self.assertEqual(node2.to_html(), "<a>This is a test!</a>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

  
if __name__ == "__main__":
    unittest.main()