from abc import abstractmethod
from typing import Callable, Any

from src.core.environment import Environment
from src.core.syntax.syntax_tree_define import SyntaxTree

_EVAL_FUNC = Callable[[Environment], Any]
_ANALYSE_FUNC = Callable[[SyntaxTree | Any], _EVAL_FUNC]


class AnalyseProduce:

    def __init__(self, eval_func: _ANALYSE_FUNC):
        """通过 eval_func 回调避免循环依赖"""
        super().__init__()
        self._eval_func = eval_func

    @property
    def analyse(self) -> _ANALYSE_FUNC:
        return self._eval_func

    @abstractmethod
    def apply(self, expr: SyntaxTree | Any):
        pass
