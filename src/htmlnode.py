class HTMLnode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html
        
    def __repr__(self):
        return f"HTMLnode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        return (self.tag == other.tag and 
                self.value == other.value and
                self.children == other.children and
                self.props == other.props
        )
    
class LeafNode(HTMLnode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
         if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
         if self.tag is None:
             return self.value
         return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

   
    def __repr__(self):
        return f"HTMLnode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLnode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag cannot be empty")
        if self.children is None:
            raise ValueError("The node has no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        