from htmlnode import HTMLNode
from textnode import TextNode, TextType

if __name__ == "__main__":
    text_node = TextNode("test", TextType.LINK, "https://boot.dev")
    print(text_node)
    html_node = HTMLNode(
        "<p>",
        "this is paragraph",
        [],
        {
            "href": "https://www.google.com",
            "target": "_blank",
        },
    )
    print(html_node)
