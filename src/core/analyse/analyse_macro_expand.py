from typing import Any, Callable

from src.core.environment import Environment
from src.core.analyse.analyse_proc import AnalyseProduce
from src.core.primitive_procedure import LambdaProcedure
from src.core.syntax.syntax_tree_define import SyntaxTree


class AnalyseMacroExpandProduce(AnalyseProduce):

    def apply(self, expr: SyntaxTree | Any) -> Callable[[Environment], Any]:
        args = SyntaxTree.flat(expr.remain())

        def _exec(env) -> str:
            lambda_proc: LambdaProcedure = env.lookup_variable_value(expr.first())
            lambda_body: SyntaxTree | Any = lambda_proc.body().first()
            new_env = lambda_proc.mk_new_env(args, env)

            return str(self.analyse(lambda_body)(new_env))

        return _exec
