"""
import ast

def process_ast_node(node):
    # Check if the node is a function call
    if isinstance(node, ast.Call):
        # Return a string representation of the function call
        return ast.unparse(node) 
    else:
        # Convert the node to source code and evaluate to get the value
        node_str = ast.unparse(node)
        return eval(node_str)

        
def parse_python_function_call(call_str):
    tree = ast.parse(call_str)
    expr = tree.body[0]

    call_node = expr.value
    function_name = (
        call_node.func.id
        if isinstance(call_node.func, ast.Name)
        else str(call_node.func)
    )

    parameters = {}
    noNameParam = []

    # Process positional arguments
    for arg in call_node.args:
        noNameParam.append(process_ast_node(arg))

    # Process keyword arguments
    for kw in call_node.keywords:
        parameters[kw.arg] = process_ast_node(kw.value)

    if noNameParam:
        parameters["None"] = noNameParam
        
    function_dict = {"name": function_name, "arguments": parameters}
    return function_dict

if __name__ == "__main__":
    call_str = "func(1, [1, 2], 3, a=4, b=5)"
    print(parse_python_function_call(call_str))

    call_str = "func('cde', x=1, b='2', c=[1, 2, {'a': 1, 'b': 2}])"
    print(parse_python_function_call(call_str))

    call_str = "get_current_weather(location='Boston, MA', api_key=123456789, unit='fahrenheit')"
    print(parse_python_function_call(call_str))

"""

import ast

code = """
import math
def _generate_resolution_shells(low, high):
    \"\"\"Generate 9 evenly spaced in reciprocal space resolution shells from low to high resolution, e.g. in 1/d^2.\"\"\"
    dmin = (1.0 / high) * (1.0 / high)
    dmax = (1.0 / low) * (1.0 / low)
    diff = (dmin - dmax) / 8.0
    shells = [1.0 / math.sqrt(dmax)]
    for j in range(8):
        shells.append(1.0 / math.sqrt(dmax + diff * (j + 1)))
    return shells
"""

class FunctionSignatureVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        func_name = node.name
        params = [arg.arg for arg in node.args.args]
        print(f"def {func_name}({', '.join(params)})")

tree = ast.parse(code)
visitor = FunctionSignatureVisitor()
visitor.visit(tree)