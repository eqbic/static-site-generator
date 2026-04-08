from textnode import TextNode, TextType

if __name__ == "__main__":
    text_node = TextNode("test", TextType.LINK, "https://boot.dev")
    print(text_node)
