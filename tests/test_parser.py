import pytest

from src.syntax_parser.parser import Parser
from src.syntax_parser.tokenizer import Tokenizer

tokenizer = Tokenizer()
parser = Parser()


def test_boolean():
    assert str(parser.parse(tokenizer.tokenize("(or #f #t)"))) == "(or #f #t)"


def test_define():
    assert str(parser.parse(tokenizer.tokenize("(define size 2)"))) == "(define size 2)"
    assert str(parser.parse(tokenizer.tokenize("(define (square x)   (* x x))"))) == "(define (square x) (* x x))"


def test_let():
    assert str(parser.parse(tokenizer.tokenize("(let ((x 2) (y 3)) (+ x y))"))) == "(let ((x 2) (y 3)) (+ x y))"


def test_quote():
    assert str(parser.parse(tokenizer.tokenize("(len '(1 2 3 4))"))) == "(len (quote (1 2 3 4)))"
    assert str(parser.parse(tokenizer.tokenize("(list 'a 'b)"))) == "(list (quote a) (quote b))"
    assert str(parser.parse(tokenizer.tokenize("(quote (+ x 2))"))) == "(quote (+ x 2))"
    assert str(parser.parse(tokenizer.tokenize("'(+ x 2)"))) == "(quote (+ x 2))"


def test_nil():
    assert str(parser.parse(tokenizer.tokenize("(if nil 1 2)"))) == "(if () 1 2)"


def test_unexpect_token():
    with pytest.raises(SyntaxError):
        parser.parse(["(", "(", "define", "size", "2", ")"])


def test_unexpect_token_2():
    with pytest.raises(SyntaxError):
        parser.parse(["￥", "(", "define", "size", "2", ")"])
