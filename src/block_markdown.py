from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    UNORDERED = "unordered"
    ORDERED = "ordered"
    QUOTE = "quote"

def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    final_blocks = []
    for section in sections:
        if section.strip() != "":
            final_blocks.append(section.strip()) 

    return final_blocks


def block_to_block_type(markdown_text):
    if markdown_text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif markdown_text.startswith("```\n") and markdown_text.endswith("```"):
        return BlockType.CODE
    
    lines = markdown_text.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):    
        return BlockType.UNORDERED
    
    is_ordered = True
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i+1}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED
    
    return BlockType.PARAGRAPH    

    

    
   