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
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"alt": text_node.text, "src": text_node.url}
            )
        case _:
            raise ValueError("Unknown TextType.")
