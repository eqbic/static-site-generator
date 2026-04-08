from htmlnode import HTMLNode


class TestHtmlNode:
    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        assert node.props_to_html() == ' href="https://www.google.com" target="_blank"'

    def test_children(self):
        node_1 = HTMLNode()
        node_2 = HTMLNode()
        node_3 = HTMLNode(children=[node_1, node_2])
        assert node_3.children and len(node_3.children) == 2

    def test_props_empty_value(self):
        node = HTMLNode(
            props={
                "href": "",
                "target": "",
            }
        )
        assert node.props_to_html() == ' href="" target=""'
