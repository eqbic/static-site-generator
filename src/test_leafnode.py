from leafnode import LeafNode


class TestLeafNode:
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        assert node.to_html() == "<p>Hello, world!</p>"

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        assert node.to_html() == '<a href="https://www.google.com">Click me!</a>'
