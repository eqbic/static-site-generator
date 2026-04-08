import re
from enum import Enum


def is_heading(block: str) -> bool:
    return re.fullmatch(r"#{1,6} .*", block) is not None


def is_code(block: str) -> bool:
    return re.fullmatch(r"```\n(\w*.*\n*)*```", block) is not None


def is_quote(block: str) -> bool:
    return re.fullmatch(r"(> ?.+\n?)+", block, re.MULTILINE) is not None


def is_unordered_list(block: str) -> bool:
    return re.fullmatch(r"(- .+\n?)+", block, re.MULTILINE) is not None


def is_ordered_list(block: str) -> bool:
    lines = block.splitlines()
    for i, line in enumerate(lines, start=1):
        if not re.match(rf"^{i}\. .+", line):
            return False
    return len(lines) > 0


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

    @staticmethod
    def from_block(markdown_block: str) -> "BlockType":
        if is_heading(markdown_block):
            return BlockType.HEADING
        elif is_code(markdown_block):
            return BlockType.CODE
        elif is_quote(markdown_block):
            return BlockType.QUOTE
        elif is_unordered_list(markdown_block):
            return BlockType.UNORDERED_LIST
        elif is_ordered_list(markdown_block):
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH
