from typing import Any

from src.core.environment import Environment
from src.core.meta_procedure import MetaProcedureFactory
from src.core.primitive_procedure import Procedure, be_primitive_procedure, be_lambda_procedure, LambdaProcedure
from src.core.syntax_tree_define import SyntaxTree
from src.core.syntax_tree_recognize import be_self_evaluation, be_symbol, assert_syntax_tree, be_syntax_tree, be_nil
from src.inner_ds.pair import nil

meta_proc_factory = MetaProcedureFactory()


def k_eval(expr: SyntaxTree | str, env: Environment) -> Any:
    if be_self_evaluation(expr):
        return expr

    if be_symbol(expr):
        return env.lookup_variable_value(expr)

    assert_syntax_tree(expr)

    first, rest = expr.first(), expr.remain()

    # 元语言符号处理过程 define, if, lambda
    if be_symbol(first) and meta_proc_factory.be_exist(first):
        return meta_proc_factory.lookup(first).apply(rest, env)

    # 其他过程处理
    operator = k_eval(first, env)
    operands = rest.map(lambda x: k_eval(x, env))
    return k_apply(operator, operands, env)


def k_apply(procedure: Procedure, args: list[Any], env: Environment) -> Any:
    if be_primitive_procedure(procedure):
        return procedure.apply(args, env)

    lambda_procedure = _cast_lambda_procedure(procedure)
    new_env = lambda_procedure.mk_new_env(args, env)

    return eval_sequence(lambda_procedure.body(), new_env)


def eval_sequence(expr: SyntaxTree, env: Environment) -> Any:
    if not be_syntax_tree(expr) or be_nil(expr):
        return None

    if expr.remain() == nil:
        return k_eval(expr.first(), env)

    k_eval(expr.first(), env)
    return eval_sequence(expr.remain(), env)


def _cast_lambda_procedure(procedure: Procedure) -> LambdaProcedure:
    assert be_lambda_procedure(procedure)
    return procedure
