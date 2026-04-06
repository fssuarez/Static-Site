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