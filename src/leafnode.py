import json
from typing import override

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    @override
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf must have a value")
        if self.tag is None:
            return self.value
        html = f"<{self.tag}"
        if self.props is not None:
            for key, value in self.props.items():
                html += f' {key}="{value}"'
        html += f">{self.value}</{self.tag}>"
        return html

    @override
    def __repr__(self) -> str:
        dict_repr = {
            "tag": self.tag,
            "value": self.value,
            "children": self.children,
            "props": self.props,
        }
        repr = json.dumps(dict_repr, indent=2)
        return repr
