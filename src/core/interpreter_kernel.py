from typing import Any

from src.common_ds.pair import nil
from src.core.environment import Environment
from src.core.meta_proc.meta_proc_factory import get_meta_proc_factory
from src.core.primitive_procedure import be_primitive_procedure, be_lambda_procedure, LambdaProcedure, MacroProcedure, \
    PrimitiveProcedure, ProcedureError
from src.core.syntax.syntax_tree_define import SyntaxTree
from src.core.syntax.syntax_tree_recognize import be_self_evaluation, be_symbol, assert_syntax_tree, \
    be_syntax_tree, be_nil


def k_eval(expr: SyntaxTree | Any, env: Environment) -> Any:
    if _be_builtin_syntax(expr):
        return _process_builtin_syntax(expr, env)

    first, rest = expr.first(), expr.remain()

    app_operator = k_eval(first, env)

    if isinstance(app_operator, MacroProcedure):
        eval_body: SyntaxTree = _apply(app_operator, SyntaxTree.flat(rest), env)
        return k_eval(eval_body, env)

    operands: SyntaxTree = rest.map(lambda x: k_eval(x, env))
    return _apply(app_operator, SyntaxTree.flat(operands), env)


def _be_builtin_syntax(expr: SyntaxTree | Any):
    if not isinstance(expr, SyntaxTree):
        return True

    return _be_meta_process(expr.first())


def _process_builtin_syntax(expr: SyntaxTree | Any, env: Environment):
    """解释内部语法的语义"""
    if be_self_evaluation(expr):
        return expr

    if be_symbol(expr):
        return env.lookup_variable_value(expr)

    assert_syntax_tree(expr)

    first, rest = expr.first(), expr.remain()

    # 元语言符号处理过程 define, if, lambda
    if _be_meta_process(first):
        return _meta_factory.lookup(first).apply(rest, env)

    # 到这里一定是出现了错误
    raise ProcedureError(f"Error: unable process builtin syntax {expr}")


def _be_meta_process(first):
    return be_symbol(first) and _meta_factory.be_exist(first)


def _apply(procedure: LambdaProcedure | PrimitiveProcedure, args: list[Any], env: Environment) -> Any:
    # 对于已经预定义的py func可以直接调用
    if be_primitive_procedure(procedure):
        return procedure.apply(args, env)

    # lambda表达式 不能直接调用，必须要结合env和syntax tree重新eval参数并设置到环境中
    return _apply_lambda(_cast_lambda_procedure(procedure), args, env)


def _apply_lambda(procedure: LambdaProcedure, args: list[Any], env: Environment):
    new_env: Environment = procedure.mk_new_env(args, env)
    lambda_body = procedure.body()

    return _eval_seq(lambda_body, new_env)


def _eval_seq(expr: SyntaxTree, env: Environment) -> Any:
    if not be_syntax_tree(expr) or be_nil(expr):
        return None

    if expr.remain() == nil:
        return k_eval(expr.first(), env)

    # begin (...) (...)
    k_eval(expr.first(), env)
    return _eval_seq(expr.remain(), env)


def _cast_lambda_procedure(procedure) -> LambdaProcedure:
    assert be_lambda_procedure(procedure), f"Expect Procedure but found {procedure} type is {type(procedure)}"
    return procedure


_meta_factory = get_meta_proc_factory(lambda: k_eval)
