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


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", text)


def split_nodes(
    old_nodes: list[TextNode], extract_fn, template, type: TextType
) -> list[TextNode]:
    result = []
    for old_node in old_nodes:
        text = old_node.text
        extractions = extract_fn(text)
        if len(extractions) == 0:
            result.append(old_node)
            continue
        for extraction in extractions:
            sections = text.split(template(extraction[0], extraction[1]), 1)
            if len(sections[0]) > 0:
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(extraction[0], type, extraction[1]))
            text = sections[1]
        if len(text) > 0:
            result.append(TextNode(text, TextType.TEXT))
    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes(
        old_nodes,
        extract_markdown_links,
        lambda text, url: f"[{text}]({url})",
        TextType.LINK,
    )


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes(
        old_nodes,
        extract_markdown_images,
        lambda alt, src: f"![{alt}]({src})",
        TextType.IMAGE,
    )


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        parts = [
            TextNode(text, text_type if i % 2 == 1 else TextType.TEXT)
            for i, text in enumerate(old_node.text.split(delimiter))
            if text != ""
        ]
        result.extend(parts)
    return result


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
