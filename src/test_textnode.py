from textnode import TextNode, TextType


class TestTextNode:
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        assert node == node2

    def test_url_none(self):
        node = TextNode("this is a test", TextType.IMAGE, url=None)
        node2 = TextNode("this is a test", TextType.IMAGE, url=None)
        assert node == node2

    def test_unequal_text(self):
        node = TextNode("this is a", TextType.PLAIN)
        node2 = TextNode("this is b", TextType.PLAIN)
        assert node != node2

    def test_unqual_type(self):
        node = TextNode("this is a", TextType.BOLD)
        node2 = TextNode("this is a", TextType.CODE)
        assert node != node2
