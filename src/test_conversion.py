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
