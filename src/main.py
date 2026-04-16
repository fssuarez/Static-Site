import os
import sys
import shutil
from markdown_utils import generate_pages_recursive

# Check the length of the typed commands, if there are 2 or more items it takes the value of the second one
# if not defaults to "/"
basepath = sys.argv[1] if len(sys.argv)>1 else "/"


def copy_static_public(src, dst):
    
    if not os.path.exists(dst):
        os.mkdir(dst)
    for directory in os.listdir(src):
        source = os.path.join(src, directory)
        destination = os.path.join(dst, directory)
        if os.path.isfile(source):
            shutil.copy(source, destination)
        else:
            copy_static_public(source, destination)

def main():
    docs_path = "./docs"
    static_path = "./static"
    if os.path.exists(docs_path):
        shutil.rmtree(docs_path)
    os.mkdir(docs_path)

    copy_static_public(static_path, docs_path)
    generate_pages_recursive ("./content/", "template.html", docs_path, basepath)

if __name__ == "__main__":
    main()