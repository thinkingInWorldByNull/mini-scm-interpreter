from typing import Any

from src.core.environment import Environment
from src.core.syntax.syntax_tree_define import SyntaxTree


class Promise:
    def __init__(self, expr: SyntaxTree, env: Environment):
        self._expr = expr
        self._env = env
        self._be_done = False
        self._val = None

    @property
    def expr(self) -> SyntaxTree:
        return self._expr

    @property
    def env(self) -> Environment:
        return self._env

    def done(self, val: Any):
        self._val = val
        self._be_done = True

    def be_done(self) -> bool:
        return self._be_done

    def val(self) -> Any:
        return self._val

    def __str__(self):
        return "#[promise ({0} been eval)]".format("not " if not self._be_done else "")

    def __repr__(self) -> str:
        if self._expr.first() == "define":
            return self._expr.remain().first().first()
        else:
            return repr(self._expr)
