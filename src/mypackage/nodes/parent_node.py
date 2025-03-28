from typing import List, Optional, Dict
from src.mypackage.nodes.html_node import HTMLNode

class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: List[HTMLNode],
        props: Optional[Dict[str, any]] = None
    ) -> None:
        if tag is None:
            raise ValueError("👨‍👩‍👧parent tag is feeling naked, give it a tag, my dude!👨‍👩‍👧")
        if children is None or len(children) == 0:
            raise ValueError("👨‍👩‍👧‍👦family matters!!! this parent needs at least one child👨‍👩‍👧‍👦")
        super().__init__(
            tag = tag, 
            value = None, 
            children = children, 
            props = props
        )
    
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("👨‍👩‍👧parent tag is feeling naked, give it a tag, my dude!👨‍👩‍👧")
        if not self.children:
            raise ValueError("👨‍👩‍👧‍👦family matters!!! this parent needs at least one child👨‍👩‍👧‍👦")
        children_html = "".join(child.to_html() for child in self.children)
        props_string = self.props_to_html()
        return f"<{self.tag}{props_string}>{children_html}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"ParentNode(tag={self.tag!r}, children={self.children!r}, props={self.props!r})"