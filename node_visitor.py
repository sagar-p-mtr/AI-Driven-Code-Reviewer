import ast

class VariableCounter(ast.NodeVisitor):
    """Counts variable assignments"""

    def __init__(self):
        self.count = 0
        self.variables = []

    def visit_Assign(self, node):
        # Count each assignment
        self.count += 1

        # Get variable names
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.append(target.id)

        self.generic_visit(node)

code = """
x = 5
y = 10
name = "Alice"
result = x + y
total = 100
"""

tree = ast.parse(code)
