import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_single_props_to_html(self):
        node = HTMLNode("link", "value which is a link", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_multiple_props_to_html(self):
        node = HTMLNode("a", "click me", props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')

    def test_no_props_to_html(self):
        node = HTMLNode("div", "content", props={})
        self.assertEqual(node.props_to_html(), '')

    def test_none_props_to_html(self):
        node = HTMLNode("p", "text")
        self.assertEqual(node.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()
