import re

from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType


def from_bold(input: str) -> str:
    return re.sub(r"\*\*(.*?)\*\*", r"\1", input)


def from_italic(input: str) -> str:
    return re.sub(r"_(.*?)_", r"\1", input)


def from_code(input: str) -> str:
    return re.sub(r"`(.*?)`", r"\1", input)


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            text = from_bold(text_node.text)
            return LeafNode(tag="b", value=text)
        case TextType.ITALIC:
            text = from_italic(text_node.text)
            return LeafNode(tag="i", value=text)
        case TextType.CODE:
            text = from_code(text_node.text)
            return LeafNode(tag="code", value=text)
        case _:
            raise ValueError("Unknown TextType.")
