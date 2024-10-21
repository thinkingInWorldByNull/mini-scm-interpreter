from typing import Any

from src.core.environment import Environment
from src.core.meta_proc.meta_proc import MetaProduce
from src.core.primitive_procedure import MacroProcedure
from src.core.syntax.syntax_tree_define import SyntaxTree


class MacroMetaProduce(MetaProduce):

    def apply(self, expr: SyntaxTree | Any, env: Environment):
        func_name = expr.first()

        env.define_variable(var_name=func_name, var_val=_mk_macro_procedure(expr, env))

        return func_name


def _mk_macro_procedure(expr: SyntaxTree, env: Environment):
    parameters: SyntaxTree = expr.remain().first()
    macro_body: SyntaxTree = expr.remain().remain()

    return MacroProcedure(params=parameters, body=macro_body, env=env)
