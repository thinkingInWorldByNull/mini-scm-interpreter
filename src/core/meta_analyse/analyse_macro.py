from typing import Any, Callable

from src.core.environment import Environment
from src.core.meta_analyse.analyse_proc import AnalyseProduce
from src.core.primitive_procedure import MacroProcedure
from src.core.syntax.syntax_tree_define import SyntaxTree


class AnalyseMacroProduce(AnalyseProduce):

    def apply(self, expr: SyntaxTree | Any) -> Callable[[Environment], str]:
        func_name = expr.first()
        parameters: SyntaxTree = expr.remain().first()
        macro_body: SyntaxTree = expr.remain().remain()

        def _mk_macro_procedure(env: Environment):
            return MacroProcedure(params=parameters, body=macro_body, env=env)

        def _exec(env) -> str:
            env.define_variable(var_name=func_name,
                                var_val=_mk_macro_procedure(env))

            return func_name

        return _exec
