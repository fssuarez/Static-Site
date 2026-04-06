import unittest

from htmlnode import HTMLnode


class TestHTMLnode(unittest.TestCase):
    def test_eq(self):
        node = HTMLnode("h1", "This is a test")
        node2 = HTMLnode("p", "This is a test")
        self.assertNotEqual(node, node2)
        node3 = HTMLnode("p", "This is a test")
        node4 = HTMLnode("p", "This is a test")
        self.assertEqual(node3, node4)


if __name__ == "__main__":
    unittest.main()