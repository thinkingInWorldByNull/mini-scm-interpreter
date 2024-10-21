from src.core.environment import Environment
from src.core.eval_sys import mk_eval_with_empty_env, mk_eval_with_env, mk_eval_with_extend, mk_eval_stream
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


def test_eval_stream():
    res = list(mk_eval_stream([
        "(define (square x) (* x x))",
        "(square 3)"
    ]))

    assert res == ["square", 9]


def test_set_stream():
    res = list(mk_eval_stream([
        "(set x 3)",
        "x"
    ]))

    assert res == ["x", 3]


def test_macro_stream():
    res = list(mk_eval_stream([
        "(defmacro set_var_3! (x) (list 'set x 3))",
        "(set_var_3! y)",
        "y"
    ]))
    assert res == ["set_var_3!", "y", 3]

    res = list(mk_eval_stream([
        "(defmacro double_when_cond! (x) (list 'if (= x 5) 10 (+ x 1)))",
        "(double_when_cond! 5)",
        "(double_when_cond! 12)",

    ]))
    assert res == ["double_when_cond!", 10, 13]


def test_macro_expand():
    res = list(mk_eval_stream([
        "(defmacro setx! (x) (list 'set x 3))",
        "(setx! y)",
        "y",
        "(macroexpand setx! y)",
    ]))
    assert res == ['setx!', 'y', 3, '(set y 3)']


def test_delay():
    res = list(mk_eval_stream([
        "(define x (delay (+ 1 2 (max -3 6 9))))",
        "(force x)",
    ]))

    assert res == ['x', 12]
