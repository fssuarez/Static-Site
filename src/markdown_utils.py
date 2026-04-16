from markdown_to_html import markdown_to_html_node
from htmlnode import HTMLnode
import os
import shutil
from pathlib import Path

def extract_title(markdown):
    text = markdown.split("\n")
    for lines in text:
        if lines.startswith("# "):
            return lines[2:].strip()
    raise Exception("There's no header in the file")

def generate_page(from_path, template_path, dest_path):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Opens the file, reads it and closes it.
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r")as f:
        template = f.read()    

    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    replacement = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    # Takes the directory removing the file "Ex: root/path/test.html" -> "root/path" 
    destiny = os.path.dirname(dest_path)

    # Compares if there's a directory, if not, the file is created in the root. "makedirs" create all the folders.
    if destiny != "":
        os.makedirs(destiny, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(replacement)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    # Create file paths
    origin = Path(dir_path_content)
    destination = Path(dest_dir_path)

    # Loop through files with extension .md
    for file in origin.rglob("*.md"):
        relative_path = file.relative_to(origin)

    # Joins the destination with the relative path. Ex: destination Public, relative path common/test final path Public/common/test
    # .with_suffix() changes the extension of the resultant file
        dest_path = destination.joinpath(relative_path).with_suffix(".html")

    # parent removes the file at the end of the path
    # parents make sure the entire folder tree is created
    # exist avoids errors if the folder already exists
     
        dest_path.parent.mkdir(parents = True, exist_ok = True)

    # origin, template, final location
        generate_page(file, template_path, dest_path)



    
