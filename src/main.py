from src.inner_ds.pair import Pair
from src.syntax_parser.parser import Parser
from src.syntax_parser.tokenizer import Tokenizer

if __name__ == '__main__':
    lst = Pair(10, Pair(12, Pair(13)))
    # print(lst)

    tokenizer = Tokenizer()
    parser = Parser()
    # print(parser.parse(tokenizer.tokenize("(define size 2)")))
    ast = parser.parse(tokenizer.tokenize("(define (abs x) (if (< x 0) (- x) x ) )"))
    print(ast)
