from src.syntax_parser.parser import Parser
from src.syntax_parser.tokenizer import Tokenizer


def test_parser():
    tokenizer = Tokenizer()
    parser = Parser()

    assert str(parser.parse(tokenizer.tokenize("(define (square x)   (* x x))"))) == "(define (square x) (* x x))"
