from typing import override

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list["HTMLNode"], props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    @override
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if self.children and len(self.children) == 0:
            raise ValueError("ParentNode must have child nodes.")
        html = f"<{self.tag}"
        if self.props:
            for key, value in self.props.items():
                html += f' {key}="{value}"'
        html += ">"
        if self.children:
            for child in self.children:
                html += child.to_html()
        html += f"</{self.tag}>"
        return html
