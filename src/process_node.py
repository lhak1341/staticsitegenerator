import re

from textnode import TextNode, TextType


# node = TextNode("This is text with a `code block` word", TextType.TEXT)
# new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
# [
#     TextNode("This is text with a ", TextType.TEXT),
#     TextNode("code block", TextType.CODE),
#     TextNode(" word", TextType.TEXT)
# ]
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

# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# extracts = extract_markdown_images(text)
# [
#     ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
#     ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
# ]
def extract_markdown_images(text):
    pattern = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(pattern, text)
    return matches

# text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
# extracts = extract_markdown_links(text)
# [
#     ("to boot dev", "https://www.boot.dev"),
#     ("to youtube", "https://www.youtube.com/@bootdotdev")
# ]
def extract_markdown_links(text):
    pattern = r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(pattern, text)
    return matches

# node = TextNode(
#     "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
#     TextType.TEXT,
# )
# new_nodes = split_nodes_link([node])
# [
#     TextNode("This is text with a link ", TextType.TEXT),
#     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
#     TextNode(" and ", TextType.TEXT),
#     TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
# ]
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
      if old_node.text_type != TextType.TEXT:
          new_nodes.append(old_node)
      else:
          extracts = extract_markdown_links(old_node.text)
          if len(extracts) == 0:
              new_nodes.append(old_node)
          else:
              process_text = old_node.text
              for extract in extracts:
                  link_text, link_url = extract
                  sections = process_text.split(f"[{link_text}]({link_url})", 1)
                  if sections[0] != "":
                      new_nodes.append(TextNode(sections[0], TextType.TEXT))
                  new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                  process_text = sections[1]
              if process_text != "":
                  new_nodes.append(TextNode(process_text, TextType.TEXT))
    return new_nodes

# node = TextNode(
#     "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
#     TextType.TEXT,
# )
# new_nodes = split_nodes_image([node])
# [
#     TextNode("This is text with an ", TextType.TEXT),
#     TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
#     TextNode(" and another ", TextType.TEXT),
#     TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
# ]
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            extracts = extract_markdown_images(old_node.text)
            if len(extracts) == 0:
                new_nodes.append(old_node)
            else:
                process_text = old_node.text
                for extract in extracts:
                    image_text, image_url = extract
                    sections = process_text.split(f"![{image_text}]({image_url})", 1)
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))
                    process_text = sections[1]
                if process_text != "":
                    new_nodes.append(TextNode(process_text, TextType.TEXT))
    return new_nodes

# text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
# new_nodes = text_to_textnodes(text)
# [
#     TextNode("This is ", TextType.TEXT),
#     TextNode("**text**", TextType.BOLD),
#     TextNode(" with an ", TextType.TEXT),
#     TextNode("_italic_", TextType.ITALIC),
#     TextNode(" word and a ", TextType.TEXT),
#     TextNode("`code block`", TextType.CODE),
#     TextNode(" and an ", TextType.TEXT),
#     TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
#     TextNode(" and a ", TextType.TEXT),
#     TextNode("link", TextType.LINK, "https://boot.dev"),
# ]
def text_to_textnodes(text):
    split_bold = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    split_link = split_nodes_link(split_code)
    new_nodes = split_nodes_image(split_link)
    return new_nodes
