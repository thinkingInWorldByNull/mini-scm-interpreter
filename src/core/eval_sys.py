from src.core.environment import Environment
from src.core.interpreter_kernel import k_eval
from src.core.primitive_procedure import PrimitiveProcedure, get_primitive_proc
from src.core.syntax.syntax_tree_define import SyntaxTree
from src.syntax_parser.parser import Parser
from src.syntax_parser.tokenizer import Tokenizer

tokenizer = Tokenizer()
parser = Parser()


def mk_eval_with_empty_env(expr: str):
    return mk_eval_with_env(expr, Environment())


def mk_eval_with_extend(expr: str,
                        extend_primitive: dict[str, PrimitiveProcedure] = None,
                        be_allow_override_built_in: bool = False):
    return mk_eval_with_env(expr, _merge_env(be_allow_override_built_in, extend_primitive))


def mk_eval_with_env(expr: str, env: Environment):
    ast = parser.parse(tokenizer.tokenize(expr))
    tree = SyntaxTree.from_pair_parser(ast)
    return k_eval(tree, env)


def mk_eval_stream(express: list[str],
                   extend_primitive: dict[str, PrimitiveProcedure] = None,
                   be_allow_override_built_in: bool = False):
    env = _merge_env(be_allow_override_built_in, extend_primitive)

    for expr in express:
        yield mk_eval_with_env(expr, env)


def _merge_env(be_allow_override_built_in: bool, extend_primitive: dict[str, PrimitiveProcedure]):
    built_in_proc = get_primitive_proc()
    extend_primitive = extend_primitive or {}

    _check_overwrite(be_allow_override_built_in, built_in_proc, extend_primitive)

    return Environment.init_from_dict(built_in_proc | extend_primitive)


def _check_overwrite(be_allow_override_built_in: bool,
                     built_in_proc: dict[str, PrimitiveProcedure],
                     extend_primitive: dict[str, PrimitiveProcedure]):
    if be_allow_override_built_in:
        for k in extend_primitive.keys():
            built_in_proc.pop(k)
        return

    for k in built_in_proc.keys():
        if k in extend_primitive and not be_allow_override_built_in:
            raise Exception("Do you want override built in func ? if true please set be_allow_override_built_in=True")
