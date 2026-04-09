import re

from blocktype import BlockType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
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


def extract_markdown_heading(header: str) -> tuple[int, str]:
    match = re.match(r"^(#{1,6}) (.+)", header)
    level = len(match.group(1))
    text = match.group(2)
    return (level, text)


def extract_title(markdown: str) -> str:
    match = re.match(r"(#{1} )(.+)", markdown.strip())
    if match:
        title = match.group(2)
        return title
    raise ValueError("No title found in markdown file.")


def extract_paragraph(block: str) -> str:
    return " ".join(line.strip() for line in block.splitlines())


def extract_quote(block: str) -> str:
    match = re.fullmatch(r"(> ?)(.+)", block, re.MULTILINE)
    return match.group(2)


def extract_unordered_list(block: str) -> list[str]:
    lines = block.splitlines()
    items = []
    for line in lines:
        match = re.match("(- )(.+)", line)
        if match:
            items.append(match.group(2))
    return items


def extract_ordered_list(block: str) -> list[str]:
    lines = block.splitlines()
    items = []
    for line in lines:
        match = re.match(r"(\d. )(.+)", line)
        if match:
            items.append(match.group(2))
    return items


def extract_code(block: str) -> str:
    return "\n".join(line.strip() for line in block.splitlines()[1:-1]) + "\n"


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


def text_to_text_nodes(text: str) -> list[TextNode]:
    result = [TextNode(text, TextType.TEXT)]
    result = split_nodes_delimiter(result, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_link(result)
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


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if len(block) > 0]


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    block_elements = []
    for block in blocks:
        block_type = BlockType.from_block(block)
        match block_type:
            case BlockType.PARAGRAPH:
                text = extract_paragraph(block)
                text_nodes = text_to_text_nodes(text)
                leafs = [text_node_to_html_node(node) for node in text_nodes]
                p_node = ParentNode("p", leafs)
                block_elements.append(p_node)
            case BlockType.HEADING:
                level, text = extract_markdown_heading(block)
                text_nodes = text_to_text_nodes(text)
                leafs = [text_node_to_html_node(node) for node in text_nodes]
                h_node = ParentNode(f"h{level}", leafs)
                block_elements.append(h_node)
            case BlockType.CODE:
                code = extract_code(block)
                text_nodes = [TextNode(code, TextType.TEXT)]
                leafs = [text_node_to_html_node(node) for node in text_nodes]
                code_node = ParentNode("code", leafs)
                block_elements.append(ParentNode("pre", [code_node]))
            case BlockType.QUOTE:
                quote_text = extract_quote(block)
                text_nodes = text_to_text_nodes(quote_text)
                leafs = [text_node_to_html_node(node) for node in text_nodes]
                quote_node = ParentNode("blockquote", leafs)
                block_elements.append(quote_node)
            case BlockType.UNORDERED_LIST:
                entries = extract_unordered_list(block)
                li_elements = []
                for entry in entries:
                    text_nodes = text_to_text_nodes(entry)
                    leafs = [text_node_to_html_node(node) for node in text_nodes]
                    li_node = ParentNode("li", leafs)
                    li_elements.append(li_node)
                ol_parent = ParentNode("ul", li_elements)
                block_elements.append(ol_parent)
            case BlockType.ORDERED_LIST:
                entries = extract_ordered_list(block)
                li_elements = []
                for entry in entries:
                    text_nodes = text_to_text_nodes(entry)
                    leafs = [text_node_to_html_node(node) for node in text_nodes]
                    li_node = ParentNode("li", leafs)
                    li_elements.append(li_node)
                ol_parent = ParentNode("ol", li_elements)
                block_elements.append(ol_parent)
            case _:
                raise ValueError("Unknown BlockType")

    parent = ParentNode("div", children=block_elements)
    return parent
