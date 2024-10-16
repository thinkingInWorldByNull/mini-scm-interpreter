"""
元语言处理过程包括处理 define, lambda, if, let, or, and, macro等
"""
from abc import abstractmethod
from typing import Any, Callable

from src.core.environment import Environment
from src.core.primitive_procedure import ProcedureError, LambdaProcedure
from src.core.syntax_tree_define import SyntaxTree
from src.core.syntax_tree_recognize import be_symbol, assert_syntax_tree


def _make_lambda(parameters, body) -> SyntaxTree:
    return SyntaxTree("lambda", SyntaxTree(parameters, body))


class MetaProcedure:
    @abstractmethod
    def apply(self, arg: SyntaxTree, env: Environment) -> Any:
        pass


class DefinitionMetaProcedure(MetaProcedure):

    def __init__(self, eval_function: Callable[[SyntaxTree, Environment], Any]):
        super().__init__()
        self._eval_function = eval_function

    @staticmethod
    def _definition_name(tree: SyntaxTree) -> str:
        target: SyntaxTree | str = tree.first()

        if be_symbol(target):
            return target

        assert_syntax_tree(target)

        if be_symbol(target.first()):
            return target.first()

        raise ProcedureError("Non symbol find")

    @staticmethod
    def _definition_val(tree: SyntaxTree) -> SyntaxTree:
        target: SyntaxTree | str = tree.first()

        # (define size 2)
        if be_symbol(target):
            return tree.remain().first()

        assert_syntax_tree(target)

        # (define (square x) (* x x))
        if be_symbol(target.first()):
            return _make_lambda(target.remain(), tree.remain())

        raise ProcedureError("Non symbol find")

    def apply(self, tree: SyntaxTree, env: Environment) -> str:
        name: str = self._definition_name(tree)
        val: SyntaxTree = self._definition_val(tree)

        env.define_variable(name, self._eval_function(val, env))

        return name


class LambdaMetaProcedure(MetaProcedure):

    def apply(self, tree: SyntaxTree, env: Environment) -> LambdaProcedure:
        parameters: SyntaxTree = tree.first()
        body: SyntaxTree = tree.remain()

        return LambdaProcedure(parameters, body, env)


class MetaProcedureFactory:

    def __init__(self):
        self._factory: dict[str, MetaProcedure] = {}

    def register(self, name: str, meta_proc: MetaProcedure):
        if name in self._factory:
            raise ProcedureError(f"{name} is conflict, please consider change name!")

        self._factory[name] = meta_proc

    def be_exist(self, expr: str) -> bool:
        return expr in self._factory

    def lookup(self, expr: str) -> MetaProcedure:
        return self._factory[expr]
