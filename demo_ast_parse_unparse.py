import ast

messy = "def hello(x, y):return x+y"

tree = ast.parse(messy)
print(ast.unparse(tree))