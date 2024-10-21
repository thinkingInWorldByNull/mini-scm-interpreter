from typing import Any

from src.core.environment import Environment
from src.core.meta_proc.meta_proc import MetaProduce
from src.core.primitive_procedure import LambdaProcedure
from src.core.syntax.syntax_tree_define import SyntaxTree


class MacroExpandMetaProduce(MetaProduce):

    def apply(self, expr: SyntaxTree | Any, env: Environment):
        lambda_proc: LambdaProcedure = env.lookup_variable_value(expr.first())
        args = SyntaxTree.flat(expr.remain())

        return str(self.eval(lambda_proc.body().first(), lambda_proc.mk_new_env(args, env)))