from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        selections = old_node.text.split(delimiter)
        if len(selections) % 2 == 0:
            raise ValueError("Invalid Markdown, formatted section not closed")
        for i in range(len(selections)):
            if selections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(selections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(selections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
