import unittest

from block import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_paragraph(self):
        block = "This is a **normal** block"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = "```\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote\n> From an author"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_not(self):
        block = "> This is a quote\nFrom an author"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_not(self):
        block = "1. Line 1\n3. Line 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
