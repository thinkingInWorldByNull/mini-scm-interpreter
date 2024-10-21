from typing import Any, Callable

from src.core.environment import Environment
from src.core.meta_analyse.analyse_proc import AnalyseProduce
from src.core.syntax.syntax_tree_define import SyntaxTree


class AnalyseIfProduce(AnalyseProduce):

    def apply(self, expr: SyntaxTree | Any) -> Callable[[Environment], bool]:
        predict = expr.first()

        def _exec(env):
            if predict_value := self.analyse(predict)(env):
                return self._eval_if_body(predict_value, expr, env)

            elif _be_exist_if_alternative(expr):
                return self.analyse(_get_if_alternative(expr))(env)
            else:
                return False

        return _exec

    def _eval_if_body(self, predict_value: Any, expr: SyntaxTree, env: Environment):
        if_body = _get_if_body(expr)

        if SyntaxTree.be_nil(if_body):
            return predict_value

        return self.analyse(if_body)(env)


def _get_if_body(expr: SyntaxTree):
    return expr.remain().first()


def _get_if_alternative(expr: SyntaxTree):
    return expr.remain().remain().first()


def _be_exist_if_alternative(expr):
    return not SyntaxTree.be_nil(expr.remain().remain().first())
