from typing import Any, Dict, List, Optional

class HTMLNode:
    def __init__(
            self, 
            tag: Optional[str] = None, 
            value: Optional[str]= None, 
            children:Optional[List['HTMLNode']] = None, 
            props:Optional[Dict[str, Any]] = None
        ) -> None:
            self.tag:Optional[str] = tag
            self.value:Optional[str] = value
            self.children:List[HTMLNode] = children if children is not None else []
            self.props: Dict[str, Any] = props if props is not None else {}
    
    def to_html(self):
        raise NotImplementedError("sub classes should implement to_html() my dude")
    
    def props_to_html(self):
        if not self.props:
            return ""
        attributes = " ".join(f'{k}="{v}"' for k, v in self.props.items())
        return f" {attributes}"
    # repr has a cool conversion 
    # tag https://dev.to/behainguyen/python-the-r-string-format-and-the-repr-and-str-methods-29i7
    def __repr__(self) -> str:
         return (
            f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
            f"children={self.children!r}, props={self.props!r})"
        )