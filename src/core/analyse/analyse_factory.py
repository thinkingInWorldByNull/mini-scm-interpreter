# 元语言处理过程包括处理 define, lambda, if, let, or, and, macro等

from typing import Any, Callable

from src.core.environment import Environment
from src.core.analyse.analyse_define import AnalyseDefineProduce
from src.core.analyse.analyse_delay import AnalyseDelayProduce
from src.core.analyse.analyse_if import AnalyseIfProduce
from src.core.analyse.analyse_lambda import AnalyseLambdaProduce
from src.core.analyse.analyse_macro import AnalyseMacroProduce
from src.core.analyse.analyse_macro_expand import AnalyseMacroExpandProduce
from src.core.analyse.analyse_proc import AnalyseProduce
from src.core.analyse.analyse_quote import AnalyseQuoteProduce
from src.core.analyse.analyse_set import AnalyseSetProduce
from src.core.primitive_procedure import ProcedureError
from src.core.syntax.syntax_tree_define import SyntaxTree

_EVAL_FUNC = Callable[[Environment], Any]
_ANALYSE_FUNC = Callable[[SyntaxTree | Any], _EVAL_FUNC]


class AnalyseProcedureFactory:

    def __init__(self):
        self._factory: dict[str, AnalyseProduce] = {}

    def register(self, name: str, meta_proc: AnalyseProduce):
        if name in self._factory:
            raise ProcedureError(f"{name} is conflict, please consider change name!")

        self._factory[name] = meta_proc

    def be_exist(self, expr: str) -> bool:
        return expr in self._factory

    def lookup(self, expr: str) -> AnalyseProduce:
        return self._factory[expr]


def get_analyse_factory(eval_func_factory: Callable[[], _ANALYSE_FUNC]) -> AnalyseProcedureFactory:
    analyse_factory = AnalyseProcedureFactory()
    eval_fun = eval_func_factory()

    analyse_factory.register("define", AnalyseDefineProduce(eval_fun))
    analyse_factory.register("lambda", AnalyseLambdaProduce(eval_fun))
    analyse_factory.register("defmacro", AnalyseMacroProduce(eval_fun))
    analyse_factory.register("macroexpand", AnalyseMacroExpandProduce(eval_fun))
    analyse_factory.register("quote", AnalyseQuoteProduce(eval_fun))
    analyse_factory.register("delay", AnalyseDelayProduce(eval_fun))

    analyse_factory.register("set", AnalyseSetProduce(eval_fun))
    analyse_factory.register("if", AnalyseIfProduce(eval_fun))

    return analyse_factory
