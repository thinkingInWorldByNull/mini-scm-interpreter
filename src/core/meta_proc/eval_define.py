from typing import Any

from src.core.environment import Environment
from src.core.meta_proc.meta_proc import MetaProduce
from src.core.primitive_procedure import ProcedureError
from src.core.syntax.syntax_tree_define import SyntaxTree
from src.core.syntax.syntax_tree_recognize import be_symbol, assert_syntax_tree


class DefineMetaProduce(MetaProduce):
    """
    define的作用就是把表达式的值绑定到一个变量比如 (define size (+ 12 3))
    - 解析变量名
    - 对表达式求值
    - 将变量名和值绑定到环境中
    """

    def apply(self, expr: SyntaxTree | Any, env: Environment):
        var_name: str = _get_variable_name(expr)
        var_val = self._eval_value(env, expr)

        env.define_variable(var_name, var_val)

        return var_name

    def _eval_value(self, env, expr):
        expr_body = _get_variable_body(expr)
        
        return self.eval(expr_body, env)


def _get_variable_name(tree: SyntaxTree) -> str:
    target: SyntaxTree | str = tree.first()

    if be_symbol(target):
        return target

    assert_syntax_tree(target)

    if be_symbol(target.first()):
        return target.first()

    raise ProcedureError("Non symbol find")


def _get_variable_body(tree: SyntaxTree) -> SyntaxTree:
    target: SyntaxTree | str = tree.first()

    # (define size 2)
    if be_symbol(target):
        return tree.remain().first()

    assert_syntax_tree(target)

    # (define (square x) (* x x))
    if be_symbol(target.first()):
        return _make_lambda_syntax_tree(target.remain(), tree.remain())

    raise ProcedureError("Non symbol find")


def _make_lambda_syntax_tree(parameters, body) -> SyntaxTree:
    return SyntaxTree("lambda", SyntaxTree(parameters, body))
