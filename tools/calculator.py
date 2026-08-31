import ast
import operator

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}


def safe_eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        return OPS[type(node.op)](safe_eval(node.left), safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return OPS[type(node.op)](safe_eval(node.operand))
    raise ValueError("Unsupported expression")


def calculate(expression):
    try:
        tree = ast.parse(expression, mode="eval")
        return safe_eval(tree.body)
    except Exception:
        return None


def average(numbers):
    numbers = [n for n in numbers if n is not None]
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


def percentage_diff(a, b):
    if a == 0:
        return None
    return ((b - a) / a) * 100
