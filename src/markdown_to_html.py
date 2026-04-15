from htmlnode import LeafNode, HTMLnode, ParentNode
from block_markdown import block_to_block_type, markdown_to_blocks, BlockType
from textnode import TextNode
from inline_markdown import text_to_textnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            node = create_heading_block(block)
            block_nodes.append(node)
        elif block_type == BlockType.PARAGRAPH:
            node = create_paragraph_block(block)
            block_nodes.append(node)
        elif block_type == BlockType.CODE:
            node = create_code_block(block)
            block_nodes.append(node)
        elif block_type == BlockType.UNORDERED:
            node = create_unordered_block(block)
            block_nodes.append(node)
        elif block_type == BlockType.ORDERED:
            node = create_ordered_block(block)
            block_nodes.append(node)
        elif block_type == BlockType.QUOTE:
            node = create_quote_block(block)
            block_nodes.append(node)
    return ParentNode("div", block_nodes)
        



def text_to_children(text):
    html_nodes = []
    node_list = text_to_textnodes(text)
    for node in node_list:
        html_nodes.append(TextNode.text_node_to_html_node(node))
    return html_nodes

def create_heading_block(block):    
    level = len(block)-len(block.lstrip("#"))
    text = block[level+1:]
    return ParentNode(f"h{level}", text_to_children(text))

def create_paragraph_block(block):
    return ParentNode("p", text_to_children(block))

def create_quote_block(block):
    text = block.split("\n")
    new_lines = []
    for line in text:
        if line.startswith("> "):
            new_lines.append(line.lstrip("> ").strip())   
        elif line.startswith(">"):
            new_lines.append(line.lstrip(">").strip())
        
    final_text = "\n".join(new_lines)
    return ParentNode("blockquote", text_to_children(final_text))

def create_code_block(block):
    text = block.strip("```").strip(" \n")
    node = TextNode(text, "code")
    leaf = TextNode.text_node_to_html_node(node)
    return ParentNode("pre", [ParentNode("code", [leaf])])

def create_unordered_block(block):
    text = block.split("\n")
    final_list = []
    for line in text:
        if line.startswith(("- ", "* ")):
            final_list.append(ParentNode("li", text_to_children(line[2:])))
    return ParentNode("ul", final_list)


def create_ordered_block(block):
    text = block.split("\n")
    final_list = []
    for line in text:
        final_list.append(ParentNode("li", text_to_children(line[line.find(" ")+1:])))
    return ParentNode("ol", final_list)



