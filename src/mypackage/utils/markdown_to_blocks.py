def markdown_to_blocks(markdown: str) -> list:
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]