from htmlnode import HTMLNode
from typing import Optional, Dict, Any

class LeafNode(HTMLNode):
    def __init__(
            self, 
            tag: Optional[str], 
            value: str, 
            props: Optional[Dict[str, Any]] = None
        ) -> None:

        if value is None:
            raise ValueError("🍃the leaf node must have a value🍃")
    
        super().__init__(
            tag = tag, 
            value = value, 
            children = None, 
            props = props
        )
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("🍃this leaf node is supposed to have a value🍃")
        if self.tag is None:
            return self.value
        
        props_string = self.props_to_html()
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"