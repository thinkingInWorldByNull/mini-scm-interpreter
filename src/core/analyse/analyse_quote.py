from typing import Any, Callable

from src.core.environment import Environment
from src.core.analyse.analyse_proc import AnalyseProduce
from src.core.syntax.syntax_tree_define import SyntaxTree


class AnalyseQuoteProduce(AnalyseProduce):

    def apply(self, expr: SyntaxTree | Any) -> Callable[[Environment], Any]:
        res = expr.first()

        return lambda _env: res
