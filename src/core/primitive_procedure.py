"""
原语处理
1. 常见的运算符：+ - * / plus minus mul div cons len ...
2. lambda过程抽象
"""
import numbers
import operator
from functools import reduce
from typing import Callable, Any

from src.core.environment import Environment
from src.core.syntax_tree_define import SyntaxTree
from src.inner_ds.pair import Pair

PRIMITIVE_PROCS: dict[str, tuple[Callable[[list[Any]], Any], bool]] = {}


class ProcedureError(Exception):
    pass


class Procedure:
    def apply(self, args: list[Any], env: Environment):
        pass


class PrimitiveProcedure:
    pass


class LambdaProcedure(Procedure):

    def __init__(self, parameters: SyntaxTree, body: SyntaxTree, env: Environment):
        super().__init__()
        self._parameters = parameters
        self._body = body
        self._env = env

    def mk_new_env(self, args: list[Any], env: Environment):
        pass

    def body(self) -> SyntaxTree:
        pass


def be_primitive_procedure(proc: Procedure) -> bool:
    return isinstance(proc, PrimitiveProcedure)


def be_lambda_procedure(proc: Procedure) -> bool:
    return isinstance(proc, LambdaProcedure)


def primitive(name: str, use_env=False):
    def register_primitive_proces(fn):
        if name in PRIMITIVE_PROCS:
            raise ValueError(f"Occur conflict that {name} already exist, please consider change the fn name")

        PRIMITIVE_PROCS[name] = (fn, use_env)
        return fn

    return register_primitive_proces


@primitive("pair?")
def be_scheme_pair(x: Any):
    return isinstance(x, Pair)


@primitive("number?")
def be_number(x):
    return isinstance(x, numbers.Number)


def _check_nums(*vals):
    for i, v in enumerate(vals):
        if not be_number(v):
            msg = "operand {0} ({1}) is not a number"
            raise ProcedureError(msg.format(i, v))


def _arith(fn, init, vals):
    return reduce(fn, vals, init)


@primitive("+")
def add(*vals):
    return _arith(operator.add, 0, vals)


@primitive("-")
def sub(val0, *vals):
    _check_nums(val0, *vals)
    if len(vals) == 0:
        return -val0
    return _arith(operator.sub, val0, vals)


@primitive("*")
def mul(*vals):
    return _arith(operator.mul, 1, vals)


@primitive("/")
def div(val0, *vals):
    _check_nums(val0, *vals)
    try:
        if len(vals) == 0:
            return operator.truediv(1, val0)

        return _arith(operator.truediv, val0, vals)
    except ZeroDivisionError as err:
        raise ProcedureError(err)


@primitive("abs")
def _abs(val0):
    return abs(val0)
