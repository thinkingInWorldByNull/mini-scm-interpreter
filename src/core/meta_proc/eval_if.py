from typing import Any

from src.core.environment import Environment
from src.core.meta_proc.meta_proc import MetaProduce
from src.core.syntax.syntax_tree_define import SyntaxTree


class IfMetaProduce(MetaProduce):

    def apply(self, expr: SyntaxTree | Any, env: Environment):
        predict = expr.first()
        predict_value = self.eval(predict, env)

        if predict_value:
            return self._eval_if_body(predict_value, expr, env)

        elif _be_exist_if_alternative(expr):
            return self.eval(_get_if_alternative(expr), env)
        else:
            return False

    def _eval_if_body(self, predict_value: Any, expr: SyntaxTree, env: Environment):
        if_body = _get_if_body(expr)

        if SyntaxTree.be_nil(if_body):
            return predict_value

        return self.eval(if_body, env)


def _get_if_body(expr: SyntaxTree):
    return expr.remain().first()


def _get_if_alternative(expr:SyntaxTree):
    return expr.remain().remain().first()


def _be_exist_if_alternative(expr):
    return not SyntaxTree.be_nil(expr.remain().remain().first())
