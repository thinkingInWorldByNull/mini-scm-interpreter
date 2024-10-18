# 元语言处理过程包括处理 define, lambda, if, let, or, and, macro等

from typing import Any, Callable

from src.core.environment import Environment
from src.core.meta_proc.eval_define import DefineMetaProduce
from src.core.meta_proc.eval_if import IfMetaProduce
from src.core.meta_proc.eval_lambda import LambdaMetaProduce
from src.core.meta_proc.eval_macro import MacroMetaProduce
from src.core.meta_proc.eval_macro_expand import MacroExpandMetaProduce
from src.core.meta_proc.eval_quote import QuoteMetaProduce
from src.core.meta_proc.eval_set import SetMetaProduce
from src.core.meta_proc.meta_proc import MetaProduce
from src.core.primitive_procedure import ProcedureError
from src.core.syntax_tree.syntax_tree_define import SyntaxTree

_EVAL_FUNC = Callable[[SyntaxTree | Any, Environment], Any]


class MetaProcedureFactory:

    def __init__(self):
        self._factory: dict[str, MetaProduce] = {}

    def register(self, name: str, meta_proc: MetaProduce):
        if name in self._factory:
            raise ProcedureError(f"{name} is conflict, please consider change name!")

        self._factory[name] = meta_proc

    def be_exist(self, expr: str) -> bool:
        return expr in self._factory

    def lookup(self, expr: str) -> MetaProduce:
        return self._factory[expr]


def get_meta_proc_factory(eval_func_factory: Callable[[], _EVAL_FUNC]) -> MetaProcedureFactory:
    meta_proc_factory = MetaProcedureFactory()
    eval_fun: _EVAL_FUNC = eval_func_factory()

    meta_proc_factory.register("define", DefineMetaProduce(eval_fun))
    meta_proc_factory.register("lambda", LambdaMetaProduce(eval_fun))
    meta_proc_factory.register("defmacro", MacroMetaProduce(eval_fun))
    meta_proc_factory.register("macroexpand", MacroExpandMetaProduce(eval_fun))
    meta_proc_factory.register("quote", QuoteMetaProduce(eval_fun))

    meta_proc_factory.register("set", SetMetaProduce(eval_fun))
    meta_proc_factory.register("if", IfMetaProduce(eval_fun))

    return meta_proc_factory
