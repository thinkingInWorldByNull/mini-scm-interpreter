from abc import abstractmethod
from typing import Callable, Any

from src.core.environment import Environment
from src.core.syntax_tree.syntax_tree_define import SyntaxTree

_EVAL_FUNC = Callable[[SyntaxTree | Any, Environment], Any]


class MetaProduce:

    def __init__(self, eval_func: _EVAL_FUNC):
        """通过 eval_func 回调避免循环依赖"""
        super().__init__()
        self._eval_func = eval_func

    @property
    def eval(self):
        return self._eval_func

    @abstractmethod
    def apply(self, expr: SyntaxTree | Any, env: Environment):
        pass
