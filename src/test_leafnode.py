import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is bold")
        self.assertEqual(node.to_html(), "<b>This is bold</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "This is italic")
        self.assertEqual(node.to_html(), "<i>This is italic</i>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "MAGIC_NUMBER")
        self.assertEqual(node.to_html(), "<code>MAGIC_NUMBER</code>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Google Search", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Google Search</a>')

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "Some captions", {"src": "image.jpg"})
        self.assertEqual(node.to_html(), '<img src="image.jpg">Some captions</img>')
