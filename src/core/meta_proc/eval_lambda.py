from typing import Any

from src.core.environment import Environment
from src.core.meta_proc.meta_proc import MetaProduce
from src.core.primitive_procedure import LambdaProcedure
from src.core.syntax_tree.syntax_tree_define import SyntaxTree


class LambdaMetaProduce(MetaProduce):

    def apply(self, expr: SyntaxTree | Any, env: Environment):
        parameters: SyntaxTree = expr.first()
        body: SyntaxTree = expr.remain()

        return LambdaProcedure(parameters, body, env)
