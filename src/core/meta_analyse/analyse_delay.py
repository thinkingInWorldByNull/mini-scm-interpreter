from typing import Any, Callable

from src.core.environment import Environment
from src.core.meta_analyse.analyse_proc import AnalyseProduce
from src.core.syntax.promise import Promise
from src.core.syntax.syntax_tree_define import SyntaxTree


class AnalyseDelayProduce(AnalyseProduce):

    def apply(self, expr: SyntaxTree | Any) -> Callable[[Environment], Promise]:
        expr = expr.first()

        return lambda env: Promise(expr=expr, env=env)
