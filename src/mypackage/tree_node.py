from typing import Optional, Dict, Any, List
from src.mypackage.html_node import HTMLNode

class TreeNode(HTMLNode):
    def __init__(
            self,
            tag: Optional[str],
            value: Optional[str] = None,
            children: Optional[List[HTMLNode]] = None,
            props: Optional[Dict[str, Any]] = None
        ) -> None:
        if children is None:
            children = []
        if value is None and not children:
            raise ValueError("🌳 tree node must have either a value or 🧒👈 point to a child 🌳")
        
        super().__init__(
            tag=tag,
            value=value,
            children=children,
            props=props
        )

    def to_html(self) -> str:
        props_string = self.props_to_html() if self.tag else ""
        inner_html = self.value if self.value else ""
        for child in self.children:
            inner_html += child.to_html()
        if self.tag:
            return f"<{self.tag}{props_string}>{inner_html}</{self.tag}>"
        else:
            return inner_html

    def __repr__(self) -> str:
        return (f"TreeNode(tag={self.tag!r}, value={self.value!r}, "
                f"children={self.children!r}, props={self.props!r})")
