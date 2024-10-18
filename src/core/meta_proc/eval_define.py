from typing import Any

from src.core.environment import Environment
from src.core.meta_proc.meta_proc import MetaProduce
from src.core.primitive_procedure import ProcedureError
from src.core.syntax_tree.syntax_tree_define import SyntaxTree
from src.core.syntax_tree.syntax_tree_recognize import be_symbol, assert_syntax_tree


class DefineMetaProduce(MetaProduce):

    def apply(self, expr: SyntaxTree | Any, env: Environment):
        name: str = eval_define_name(expr)
        val: SyntaxTree = eval_define_val(expr)

        env.define_variable(name, self.eval(val, env))

        return name


def eval_define_name(tree: SyntaxTree) -> str:
    target: SyntaxTree | str = tree.first()

    if be_symbol(target):
        return target

    assert_syntax_tree(target)

    if be_symbol(target.first()):
        return target.first()

    raise ProcedureError("Non symbol find")


def eval_define_val(tree: SyntaxTree) -> SyntaxTree:
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
