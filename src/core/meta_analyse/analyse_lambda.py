from typing import Any, Callable

from src.core.environment import Environment
from src.core.meta_analyse.analyse_proc import AnalyseProduce
from src.core.primitive_procedure import LambdaProcedure
from src.core.syntax.syntax_tree_define import SyntaxTree


class AnalyseLambdaProduce(AnalyseProduce):

    def apply(self, expr: SyntaxTree | Any) -> Callable[[Environment], LambdaProcedure]:
        parameters: SyntaxTree = expr.first()
        body: SyntaxTree = expr.remain()

        return lambda env: LambdaProcedure(parameters, body, env)
