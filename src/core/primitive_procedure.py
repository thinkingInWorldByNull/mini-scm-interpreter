"""
原语处理
1. 常见的运算符：+ - * / plus minus mul div cons len ...
2. lambda过程抽象
"""
import numbers
import operator
from functools import reduce
from typing import Callable, Any, Optional

from src.common_ds.pair import nil
from src.core.environment import Environment
from src.core.syntax_tree.syntax_tree_define import SyntaxTree


class ProcedureError(Exception):
    pass


class Procedure:
    pass


class PrimitiveProcedure(Procedure):
    """能够直接处理和识别的语法符号：比如预定义的max, min, abs..."""

    def __init__(self, be_need_env: bool, fn: Callable):
        self.be_need_env = be_need_env
        self.fn = fn

    def apply(self, args, env: Environment):
        if (args_handle := self.args_handle()) is not None:
            args = args_handle(args)

            if self.be_need_env:
                return self.fn(args, env)
            return self.fn(args)

        if self.be_need_env:
            return self.fn(*args, env)
        return self.fn(*args)

    def args_handle(self) -> Optional[Callable]:
        return None


class LambdaProcedure(Procedure):

    def __init__(self, tree: SyntaxTree, body: SyntaxTree, env: Environment):
        self._param_names = SyntaxTree.flat(tree)
        self._body = body
        self._env = env

    def mk_new_env(self, args: list[Any], _env: Environment):
        return self._env.extend_environment(self._param_names, args)

    def body(self) -> SyntaxTree:
        return self._body


class MacroProcedure(LambdaProcedure):
    pass


def be_primitive_procedure(proc: Any) -> bool:
    return isinstance(proc, PrimitiveProcedure)


def be_lambda_procedure(proc: Any) -> bool:
    return isinstance(proc, LambdaProcedure)


_PRIMITIVE_PROCS: dict[str, PrimitiveProcedure] = {}


def primitive(name: str, be_need_env: bool = False):
    def register_primitive_proces(fn):
        if name in _PRIMITIVE_PROCS:
            raise ValueError(f"Occur conflict that {name} already exist, please consider change the fn name")

        _PRIMITIVE_PROCS[name] = PrimitiveProcedure(be_need_env, fn)
        return fn

    return register_primitive_proces


def be_number(x):
    return isinstance(x, numbers.Number)


def _check_nums(*vals):
    for i, v in enumerate(vals):
        if not be_number(v):
            msg = "operand {0} ({1}) is not a number"
            raise ProcedureError(msg.format(i, v))


def _arith(fn, init, vals):
    return reduce(fn, vals, init)


@primitive("=")
def eq(val0, val1):
    return val0 == val1


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


@primitive("max")
def _max(*args):
    return max(*args)


@primitive("min")
def _min(*args):
    return min(*args)


@primitive("nil?")
def be_nil(x):
    return x is nil or x is None


@primitive("list")
def scheme_list(*vals):
    result = nil

    for e in reversed(vals):
        result = SyntaxTree(e, result)

    return result


def get_primitive_proc() -> dict[str, PrimitiveProcedure]:
    return dict(**_PRIMITIVE_PROCS)
