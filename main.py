from htmp import Parser

with open("./examples/1_basic.htmp", "r") as f:
    source = f.read()
 
parser = Parser(source)

parser.print()