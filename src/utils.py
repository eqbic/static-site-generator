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


def from_link(input: str) -> tuple[str, str]:
    return re.findall(r"\[([^\]]+)\]\(([^)]+)\)", input)[0]


def from_image(input: str) -> tuple[str, str]:
    return re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", input)[0]


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
        case TextType.LINK:
            anchor_text, url = from_link(text_node.text)
            return LeafNode(tag="a", value=anchor_text, props={"href": url})
        case TextType.IMAGE:
            alt_text, src = from_image(text_node.text)
            return LeafNode(tag="img", value="", props={"alt": alt_text, "src": src})
        case _:
            raise ValueError("Unknown TextType.")
