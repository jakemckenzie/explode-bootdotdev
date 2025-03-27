from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def is_code_block(block: str) -> bool:
    return block.startswith("```") and block.endswith("```")

def is_heading_block(block: str) -> bool:
    if not block:
        return False

    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break

    if 1 <= count <= 6 and len(block) > count and block[count] == " ":
        return True
    return False

def is_quote_block(lines: list) -> bool:
    for line in lines:
        if not line or line[0] != ">":
            return False
    return True

def is_unordered_list_block(lines: list) -> bool:
    for line in lines:
        if len(line) < 2 or line[0] != "-" or line[1] != " ":
            return False
    return True

def is_ordered_list_block(lines: list) -> bool:
    expected = 1
    for line in lines:
        prefix = str(expected) + ". "
        if len(line) < len(prefix):
            return False
        if line[:len(prefix)] != prefix:
            return False
        expected += 1
    return True


def block_to_block_type(block: str) -> BlockType:
    if is_code_block(block):
        return BlockType.CODE

    if is_heading_block(block):
        return BlockType.HEADING

    lines = block.split("\n")
    if is_quote_block(lines):
        return BlockType.QUOTE

    if is_unordered_list_block(lines):
        return BlockType.UNORDERED_LIST

    if lines and is_ordered_list_block(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
