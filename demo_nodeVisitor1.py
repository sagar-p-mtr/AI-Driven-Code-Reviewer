import ast

class ConditionalFinder(ast.NodeVisitor):
    """
    Finds if/elif/else statements.
    """

    def __init__(self):
        self.if_count = 0
        self.else_count = 0
        self.conditionals = []

    def visit_If(self, node):
        self.if_count += 1

        has_else = len(node.orelse) > 0
        if has_else:
            self.else_count += 1

        self.conditionals.append({
            'line': node.lineno,
            'has_else': has_else
        })

        self.generic_visit(node)

code = """
def check_age(age):
    if age < 18:
        print("Minor")
    else:
        print("Adult")
    
    if age > 65:
        print("Senior")
    
    if age == 21:
        print("Special Age")
    elif age == 30:
        print("Milestone")
    else:
        print("Regular age")
"""     

tree = ast.parse(code)
finder = ConditionalFinder()
finder.visit(tree)

print(f"Total if statements: {finder.if_count}")
print(f"If statements with else: {finder.else_count}")
print("\nDetails:")
for cond in finder.conditionals:
    else_status = "with else" if cond['has_else'] else "without_else"
    print(f" Line {cond['line']}: if statement {else_status}")