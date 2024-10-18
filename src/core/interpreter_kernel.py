from typing import Any

from src.core.environment import Environment
from src.core.meta_proc.meta_proc_factory import get_meta_proc_factory
from src.core.primitive_procedure import be_primitive_procedure, be_lambda_procedure, LambdaProcedure
from src.core.syntax_tree.syntax_tree_define import SyntaxTree
from src.core.syntax_tree.syntax_tree_recognize import be_self_evaluation, be_symbol, assert_syntax_tree, \
    be_syntax_tree, be_nil
from src.inner_ds.pair import nil


def k_eval(expr: SyntaxTree | Any, env: Environment) -> Any:
    if be_self_evaluation(expr):
        return expr

    if be_symbol(expr):
        return env.lookup_variable_value(expr)

    assert_syntax_tree(expr)

    first, rest = expr.first(), expr.remain()

    # 元语言符号处理过程 define, if, lambda
    if be_symbol(first) and _meta_factory.be_exist(first):
        return _meta_factory.lookup(first).apply(rest, env)

    # application 过程处理:定义的方法、操作符等
    operator = k_eval(first, env)
    operands: SyntaxTree = rest.map(lambda x: k_eval(x, env))
    return k_apply(operator, SyntaxTree.flat(operands), env)


def k_apply(procedure, args: list[Any], env: Environment) -> Any:
    # 对于已经预定义的py func可以直接调用
    if be_primitive_procedure(procedure):
        return procedure.apply(args, env)

    # lambda表达式 不能直接调用，必须要结合env和syntax tree重新eval参数并设置到环境中
    lambda_procedure: LambdaProcedure = _cast_lambda_procedure(procedure)
    new_env: Environment = lambda_procedure.mk_new_env(args, env)

    return eval_sequence(lambda_procedure.body(), new_env)


def eval_sequence(expr: SyntaxTree, env: Environment) -> Any:
    if not be_syntax_tree(expr) or be_nil(expr):
        return None

    if expr.remain() == nil:
        return k_eval(expr.first(), env)

    k_eval(expr.first(), env)
    return eval_sequence(expr.remain(), env)


def _cast_lambda_procedure(procedure) -> LambdaProcedure:
    assert be_lambda_procedure(procedure), f"Expect LambdaProcedure but found {procedure} type is {type(procedure)}"
    return procedure


_meta_factory = get_meta_proc_factory(lambda: k_eval)
