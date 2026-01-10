import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'


# blocks = [
#     "# This is a heading",
#     "This is **bolded** paragraph",
#     "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph # on a new line",
#     "- This is a list\n- with items",
# ],
# for block in blocks:
def block_to_block_type(block):
    # start with 1-6 # characters, followed by a space
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING

    # start with 3 backticks and a newline, then end with 3 backticks
    if block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE

    lines = block.split('\n')

    # every line must start with ">" and a space
    if all(line.startswith('> ') for line in lines):
        return BlockType.QUOTE

    # every line must start with "- " followed by a space.
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    # every line block must start with a number followed by "." and a space
    # the number must start at 1 and increment by 1 for each line
    is_ordered = True
    count_ordered = 1
    for line in lines:
        if not line.startswith(f'{count_ordered}. '):
            is_ordered = False
            break
        count_ordered += 1
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
