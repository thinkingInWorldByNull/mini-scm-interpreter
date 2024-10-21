from typing import Any

from src.core.environment import Environment
from src.core.meta_proc.meta_proc import MetaProduce
from src.core.syntax.syntax_tree_define import SyntaxTree


class SetMetaProduce(MetaProduce):

    def apply(self, expr: SyntaxTree | Any, env: Environment):
        var_name = expr.first()
        var_val = self.eval(expr.remain().first(), env)

        env.define_variable(var_name=var_name, var_val=var_val)

        return var_name
