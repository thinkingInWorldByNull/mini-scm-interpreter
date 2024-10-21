from typing import Any

from src.core.environment import Environment
from src.core.meta_proc.meta_proc import MetaProduce
from src.core.syntax.syntax_tree_define import SyntaxTree


class QuoteMetaProduce(MetaProduce):

    def apply(self, expr: SyntaxTree | Any, env: Environment):
        return expr.first()
