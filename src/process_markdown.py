from block import BlockType, block_to_block_type
from htmlnode import LeafNode, ParentNode
from process_node import text_to_textnodes
from textnode import text_node_to_html_node


# # This is a heading
#
# This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
#
# - This is the first list item in a list block
# - This is a list item
# - This is another list item
def markdown_to_blocks(markdown):
    results = []
    blocks = markdown.split('\n\n')
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            results.append(stripped)
    return results

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return children

def _create_list_node(lines, tag):
    list_children = []
    for line in lines:
        parts = line.split(maxsplit=1)
        content = parts[1] if len(parts) > 1 else ''
        children = text_to_children(content)
        list_children.append(ParentNode('li', children))
    return ParentNode(tag, list_children)

def markdown_to_html_node(markdown):
    result = ParentNode('div', [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        lines = block.split('\n')
        match block_type:
            case BlockType.HEADING:
                first_line = lines[0]
                level = first_line.split(maxsplit=1)[0].count('#')
                tag = f'h{level}'
                header_text = first_line.split(maxsplit=1)[1]
                result.children.append(ParentNode(tag, text_to_children(header_text)))
            case BlockType.CODE:
                children = []
                strip_block = block.split('\n')[1:-1]
                code_text = '\n'.join(strip_block) + '\n'
                children.append(LeafNode('code', code_text))
                result.children.append(ParentNode('pre', children))
            case BlockType.QUOTE:
                quote_text = []
                for line in lines:
                    stripped = line.lstrip()
                    if stripped.startswith('>'):
                        parts = stripped.split(maxsplit=1)
                        if len(parts) == 1:
                            content = ''
                        else:
                            content = parts[1]
                        quote_text.append(content)
                    else:
                        quote_text.append(stripped)
                children = text_to_children('\n'.join(quote_text))
                result.children.append(ParentNode('blockquote', children))
            case BlockType.UNORDERED_LIST:
                result.children.append(_create_list_node(lines, 'ul'))
            case BlockType.ORDERED_LIST:
                result.children.append(_create_list_node(lines, 'ol'))
            case BlockType.PARAGRAPH:
                para_text = ' '.join(lines)
                para_text = ' '.join(para_text.split())
                children = text_to_children(para_text)
                result.children.append(ParentNode('p', children))
            case _:
                raise ValueError(f"Unknown block type: {block_type}")
    return result
