import unittest

from process_node import split_nodes_delimiter
from textnode import TextNode, TextType


class TestProcessNode(unittest.TestCase):
    def test_process_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

if __name__ == "__main__":
    unittest.main()
