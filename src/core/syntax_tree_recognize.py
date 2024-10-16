import numbers

from src.core.syntax_tree_define import SyntaxTree
from src.inner_ds.pair import nil

EXPRESSION = SyntaxTree | str


def be_bool(expr):
    return expr is True or expr is False


def be_number(x):
    return isinstance(x, numbers.Number)


def be_self_evaluation(expr) -> bool:
    return (be_bool(expr)
            or be_number(expr)
            or be_nil(expr)
            or be_symbol(expr)
            or expr is None)


def be_nil(expr):
    return expr == nil


def be_symbol(expr: EXPRESSION) -> bool:
    """是否是变量名"""
    return isinstance(expr, str) and not expr.startswith("\"")


def be_syntax_tree(expr) -> bool:
    return isinstance(expr, SyntaxTree)


def assert_syntax_tree(expr):
    assert isinstance(expr, SyntaxTree), f"Expr type error : expect SyntaxTree but find {type(expr)}"


def car(expr: EXPRESSION) -> EXPRESSION:
    return expr.car


def cdr(expr: EXPRESSION) -> EXPRESSION:
    return expr.cdr
