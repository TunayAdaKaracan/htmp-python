from modals import *



def err(msg):
    print(msg)
    exit(-1)


def print_tree(node, last=True, header=''):
    elbow = "└──"
    pipe = "│  "
    tee = "├──"
    blank = "   "
    
    print(header + (elbow if last else tee) + node.tag)
    if node.children:
        for i, child_node in enumerate(node.children):
            print_tree(child_node, header=header + (blank if last else pipe), last = (i == len(node.children)-1))

class Parser:
    def __init__(self, text):
        self.text = text
        self.i = 0
        self.line = 0
        
        self.tokens = []
    
    def advance(self):
        if self.is_end(): return '\0'
        self.i += 1
        return self.text[self.i-1]
    
    def previous(self):
        if self.is_end() or self.i == 0: return '\0'
        return self.text[self.i-1]

    def peek(self):
        if self.is_end(): return '\0'
        return self.text[self.i]
    
    def peekNext(self):
        if self.i + 1 >= len(self.text): return '\0'
        return self.text[self.i+1]
    
    def match(self, char):
        if self.peek() == char:
            self.advance()
            return True
        return False
    
    def consume(self, char):
        if self.peek() == char:
            return self.advance()
        err(f"Expected {char}, found {self.peek()}")
    
    def is_alpha(self, char):
        return char.isalphanum()
    
    def is_end(self):
        return self.i >= len(self.text)
    
    def make_string(self):
        return self.make_identifier('"')
    
    def make_identifier(self, char):
        tmp = ""
        while self.peek() != char:
            tmp += self.advance()
        
        self.consume(char)
        return tmp
    
    def print(self):
        document = self.parse()
        print_tree(document.root)
        
    def parse(self):
        document = Document()
        document.root = HTMPNode(tag="Root")
        
        current_node: HTMPNode = document.root
        
        tmp = ""
        inner_text_start = False
        while not self.is_end():
            char = self.advance()
            # Tag. Might be a begin tag or end tag
            if char == "<":
                if tmp:
                    current_node.inner_text = tmp
                    tmp = ""
                    inner_text_start = False
                
                # End tag.
                if self.match("/"):
                    # End tag can't have attributes. So we just get the tag name
                    tag_name = self.make_identifier(">")
                    if current_node.tag != tag_name:
                        err(f"Tag mismatch. Tag name {tag_name} Current Node {current_node.tag}")
                    
                    current_node = current_node.parent
                    tmp = ""
                    continue
                
                # Beginning tag.
                
                current_node = HTMPNode(parent=current_node)
                
                attr = Attribute()
                tmp = ""
                inline_tag = False
                while self.peek() != ">":
                    tmp += self.advance()
                    if self.peek() == " " and not current_node.tag:
                        current_node.tag = tmp
                        tmp = ""
                        # Eat space
                        self.advance()
                    
                    if self.previous() == " ":
                        tmp = ""
                    
                    if self.peek() == "=":
                        attr.key = tmp
                        tmp = ""
                        self.advance()
                        
                    if self.peek() == '"':
                        if not attr.key:
                            err("An attribute must have a key")
                        self.advance()
                        attr.value = self.make_string()
                        current_node.attributes.append(attr)
                        attr = Attribute()
                    
                    # Inline Tag
                    if self.peek() == "/" and self.peekNext() == ">":
                        inline_tag = True
                        if not current_node.tag:
                            current_node.tag = tmp
                
                self.advance()
                
                if inline_tag:
                    current_node = current_node.parent
                    self.advance()
                    tmp = ""
                    continue
                
                if not current_node.tag:
                    current_node.tag = tmp
                
                tmp = ""
            else:
                if char not in "    \n\t" and not inner_text_start:
                    inner_text_start = True
                if inner_text_start:
                    tmp += char
        return document