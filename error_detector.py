import ast


class ErrorFinder(ast.NodeVisitor):
    """
    WHAT IT DOES: Walks through code and finds problems like unused variables
    and unused imports.
    """
    def __init__(self):
        self.errors = []
        self.defined_vars = set()
        self.used_vars = set()
        self.imported_names = {}  # {name: line_number}
        self.builtin_names = {
            'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict',
            'set', 'tuple', 'bool', 'type', 'isinstance', 'hasattr', 'getattr',
            'setattr', 'callable', 'open', 'enumerate', 'zip', 'map', 'filter',
            'sum', 'max', 'min', 'sorted', 'reversed', 'any', 'all', 'abs',
            'round', 'pow', 'divmod', 'id', 'hash', 'hex', 'oct', 'bin',
            'ord', 'chr', 'input', 'eval', 'exec', 'compile', 'globals',
            'locals', 'vars', 'dir', 'help', 'object', 'property', 'super',
            'staticmethod', 'classmethod', 'Exception', 'ValueError', 'KeyError'
        }

    def visit_Import(self, node):
        """When we see: import x or import x as y"""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name.split('.')[0]
            self.imported_names[name] = node.lineno
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """When we see: from x import y"""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            if name != '*':  # Skip wildcard imports
                self.imported_names[name] = node.lineno
        self.generic_visit(node)

    def visit_Assign(self, node):
        """When we see: x = 5"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined_vars.add(target.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """When we see: def func_name():"""
        self.defined_vars.add(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """When we see: class ClassName:"""
        self.defined_vars.add(node.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        """When we see a variable being used"""
        if isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
        self.generic_visit(node)

    def find_unused_variables(self):
        """Find variables that are defined but never used"""
        unused = self.defined_vars - self.used_vars
        for var in unused:
            self.errors.append({
                "type": "UnusedVariable",
                "line": "Unknown",
                "message": f"Variable '{var}' is defined but never used",
                "suggestion": f"Remove '{var}' or use it in your code"
            })
        return self.errors

    def find_unused_imports(self):
        """Find imports that are not used in the code"""
        # Don't report builtins as unused imports
        for name, line_no in self.imported_names.items():
            if name not in self.used_vars and name not in self.builtin_names:
                self.errors.append({
                    "type": "UnusedImport",
                    "line": line_no,
                    "message": f"Import '{name}' is defined but never used",
                    "suggestion": f"Remove 'import {name}' or use it in your code"
                })
        return self.errors


def detect_errors(code_string):
    """Main function to detect errors in Python code"""
    try:
        tree = ast.parse(code_string)
        finder = ErrorFinder()

        finder.visit(tree)

        # Find both unused variables and unused imports
        finder.find_unused_variables()
        finder.find_unused_imports()

        return {
            "success": True,
            "errors": finder.errors,
            "error_count": len(finder.errors)
        }

    except SyntaxError as e:
        return {
            "success": True,
            "errors": [{
                "type": "SyntaxError",
                "line": e.lineno,
                "message": f"Syntax Error: {e.msg}",
                "suggestion": f"Check line {e.lineno}: {e.text.strip() if e.text else 'Invalid syntax'}"
            }],
            "error_count": 1
        }

