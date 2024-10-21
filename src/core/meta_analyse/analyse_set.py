from typing import Any, Callable

from src.core.environment import Environment
from src.core.meta_analyse.analyse_proc import AnalyseProduce
from src.core.syntax.syntax_tree_define import SyntaxTree


class AnalyseSetProduce(AnalyseProduce):

    def apply(self, expr: SyntaxTree | Any) -> Callable[[Environment], Any]:
        var_name = expr.first()
        expr_body = expr.remain().first()

        def _exec(env):
            var_val = self.analyse(expr_body)(env)
            env.define_variable(var_name=var_name, var_val=var_val)
            return var_name

        return _exec
