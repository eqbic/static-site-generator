from textnode import TextNode, TextType
from utils import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_text_nodes,
)


class TestConversion:
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        assert html_node.tag is None
        assert html_node.value == "This is a text node"

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        assert html_node.tag == "b"
        assert html_node.value == "This is bold text"

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        assert html_node.tag == "i"
        assert html_node.value == "This is italic text"

    def test_code(self):
        node = TextNode("This is hacker code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        assert html_node.tag == "code"
        assert html_node.value == "This is hacker code"

    def test_link(self):
        node = TextNode(text="link", url="https://boot.dev", text_type=TextType.LINK)
        html_node = text_node_to_html_node(node)
        assert html_node.tag == "a"
        assert html_node.value == "link"
        assert html_node.props["href"] == "https://boot.dev"

    def test_image(self):
        node = TextNode(
            text="image of a bird", url="image.png", text_type=TextType.IMAGE
        )
        html_node = text_node_to_html_node(node)
        assert html_node.tag == "img"
        assert html_node.value == ""
        assert html_node.props["src"] == "image.png"
        assert html_node.props["alt"] == "image of a bird"

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert new_nodes == [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

    def test_split_nodes_delimiter_multiple_code_beginning(self):
        node = TextNode("`This` is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert new_nodes == [
            TextNode("This", TextType.CODE),
            TextNode(" is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

    def test_split_nodes_bold(self):
        node = TextNode("This is a **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert new_nodes == [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        assert [("image", "https://i.imgur.com/zjjcJKZ.png")] == matches

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with two images: ![image_one](image1.png) and ![image_two](image2.png)"
        )
        assert [("image_one", "image1.png"), ("image_two", "image2.png")] == matches

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://boot.dev)"
        )
        assert [("link", "https://boot.dev")] == matches

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with two links: [link_one](https://boot.dev) and [link_two](https://google.com)"
        )
        assert [
            ("link_one", "https://boot.dev"),
            ("link_two", "https://google.com"),
        ] == matches

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        assert [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ] == new_nodes

    def test_split_images_beginning_end(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is an image and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        assert [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" is an image and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ] == new_nodes

    def test_split_images_no_image(self):
        node = TextNode(
            "is an image and another",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        assert [
            TextNode("is an image and another", TextType.TEXT),
        ] == new_nodes

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://boot.dev) and another [second link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        assert [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://google.com"),
        ] == new_nodes

    def test_split_links_beginning_end(self):
        node = TextNode(
            "[link](https://boot.dev) is an link and another [second link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        assert [
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" is an link and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://google.com"),
        ] == new_nodes

    def test_split_links_no_link(self):
        node = TextNode(
            "is an image and another",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        assert [
            TextNode("is an image and another", TextType.TEXT),
        ] == new_nodes

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        assert text_to_text_nodes(text) == [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line





- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        assert blocks == [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]

    def test_extract_title(self):
        md = """
# This is my tile

## This is not an title"""
        assert extract_title(md) == "This is my tile"
