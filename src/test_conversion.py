from textnode import TextNode, TextType
from utils import text_node_to_html_node


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
