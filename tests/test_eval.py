from src.core.environment import Environment
from src.core.eval_sys import mk_eval_with_empty_env, mk_eval_with_env, mk_eval_with_extend
from src.core.primitive_procedure import PrimitiveProcedure
from src.syntax_parser.parser import Parser
from src.syntax_parser.tokenizer import Tokenizer

tokenizer = Tokenizer()
parser = Parser()


def test_self_expression():
    assert mk_eval_with_empty_env("1") == 1
    assert mk_eval_with_empty_env("1.23") == 1.23

    assert mk_eval_with_empty_env("true")
    assert not mk_eval_with_empty_env("false")


def test_extend_primitive():
    env = Environment.init_from_dict({"+": AddPrimitiveProcedure()})
    assert mk_eval_with_env("(+ 1 2 3)", env) == 6


def test_mk_eval_with_extend():
    assert mk_eval_with_extend("(+ 1 2 3)") == 6
    assert mk_eval_with_extend("(- 1 2 3)") == -4
    assert mk_eval_with_extend("(* 1 2 3)") == 6
    assert mk_eval_with_extend("(abs -3)") == 3
    assert mk_eval_with_extend("(max -3 3 5)") == 5
    assert mk_eval_with_extend("(max -3 -4)") == -3
    assert mk_eval_with_extend("(min 3 6)") == 3
    assert mk_eval_with_extend("(abs (min -3 6))") == 3


class AddPrimitiveProcedure(PrimitiveProcedure):

    def __init__(self):
        super().__init__(be_need_env=False, fn=sum)

    def args_handle(self):
        return lambda args: iter(args)
