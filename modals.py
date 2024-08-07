class Attribute:
    def __init__(self, key = None, value = None):
        self.key = key
        self.value = value
    
    def __repr__(self):
        return f"<Key={self.key} Value={self.value}>"

    def __str__(self):
        return self.__repr__()
    
class HTMPNode:
    def __init__(self, tag = None, inner_text = None, parent: "HTMPNode" = None) -> None:
        self.tag = tag
        self.inner_text = inner_text
        self.attributes = []
        self.parent = parent
        self.children = []
        
        if parent:
            parent.children.append(self)
    
    def __repr__(self):
        return f"<HTMPNode {self.tag} text='{self.inner_text}' attr={self.attributes} children={self.children}>"
    
    def __str__(self):
        return self.__repr__()
        
class Document:
    def __init__(self):
        self.root = None