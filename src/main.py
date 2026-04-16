import os
import shutil
from markdown_utils import generate_pages_recursive


def copy_static_public(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    for directory in os.listdir(src):
        source = os.path.join(src, directory)
        destination = os.path.join(dst, directory)
        if os.path.isfile(source):
            shutil.copy(source, destination)
        else:
            copy_static_public(source, destination)

def main():
    copy_static_public("./static", "./public")
    generate_pages_recursive ("./content/", "template.html", "./public")

if __name__ == "__main__":
    main()