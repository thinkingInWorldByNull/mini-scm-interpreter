from typing import Any

from src.core.environment import Environment
from src.core.syntax.syntax_tree_define import SyntaxTree
from src.interpreter_analyse import k_analyse


def k_eval(expr: SyntaxTree | Any, env: Environment) -> Any:
    return k_analyse(expr)(env)
