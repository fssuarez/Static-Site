from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        sections = node.text.split(delimiter)
        split_nodes = []

        if len(sections) % 2 == 0:
            raise Exception("Invalid Markdown Syntax")
        for i in range(len(sections)):
            if sections[i] == "":
                continue

            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_list.extend(split_nodes)

    return new_list

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_list.append(node)
        else:
            current_text = node.text
            for alt, url in images:
                sections = current_text.split(f"![{alt}]({url})",1)
                if sections[0] != "":
                    new_list.append(TextNode(sections[0], TextType.TEXT))
                new_list.append(TextNode(alt, TextType.IMAGE, url))
                current_text = sections[1]
            if current_text != "":
                new_list.append(TextNode(current_text, TextType.TEXT))
           
        
    return new_list



def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
    
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_list.append(node)
        else:
            current_text = node.text
            for alt, url in links:
                sections = current_text.split(f"[{alt}]({url})", 1)
                if sections[0] != "":
                    new_list.append(TextNode(sections[0], TextType.TEXT))
                new_list.append(TextNode(alt, TextType.LINK, url))
                current_text = sections[1]
            if current_text != "":
                new_list.append(TextNode(current_text, TextType.TEXT))
    
    return new_list

def text_to_textnodes(text):
    text_list = [TextNode(text, TextType.TEXT)]
    text_list = split_nodes_delimiter(text_list, "**", TextType.BOLD)
    text_list = split_nodes_delimiter(text_list, "*", TextType.ITALIC)
    text_list = split_nodes_delimiter(text_list, "_", TextType.ITALIC)
    text_list = split_nodes_delimiter(text_list, "`", TextType.CODE)
    text_list = split_nodes_image(text_list)
    text_list = split_nodes_link(text_list)

    return text_list


            

