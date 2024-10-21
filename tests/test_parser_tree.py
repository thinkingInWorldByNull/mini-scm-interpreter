from src.core.syntax.syntax_tree_define import SyntaxTree
from src.syntax_parser.parser import Parser
from src.syntax_parser.tokenizer import Tokenizer

tokenizer = Tokenizer()
parser = Parser()


def test_convert():
    ast = parser.parse(tokenizer.tokenize("(define square (lambda (x) (* x x)))"))
    assert str(ast) == str(SyntaxTree.from_pair_parser(ast))
