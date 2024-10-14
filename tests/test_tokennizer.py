from src.syntax_parser.Tokenizer import Tokenizer

_tokenizer = Tokenizer()


def test_boolean():
    assert _tokenizer.tokenize("true")
    assert _tokenizer.tokenize("#t")
    assert _tokenizer.tokenize("(true)") == ['(', True, ')']


def test_number():
    assert _tokenizer.tokenize("(+ 1 2)") == ['(', '+', 1, 2, ')']
    assert _tokenizer.tokenize("(+ 1 2 (- 5 3 2))") == ['(', '+', 1, 2, '(', '-', 5, 3, 2, ')', ')']


def test_define():
    assert _tokenizer.tokenize("(define (abs x) (if (< x 0) (- x) x))") == ['(', 'define', '(', 'abs', 'x', ')', '(',
                                                                            'if', '(', '<', 'x', 0, ')', '(', '-', 'x',
                                                                            ')', 'x', ')', ')']
    assert _tokenizer.tokenize("(abs -2)") == ['(', 'abs', '-2', ')']
    assert (_tokenizer.tokenize("""
    (define (map proc items)
    (if (null? items)
      nil
      (cons (proc (car items))
            (map proc (cdr items)))))
        """)
            == ['(', 'define', '(', 'map', 'proc', 'items', ')', '(', 'if', '(', 'null?', 'items', ')', 'nil', '(',
                'cons', '(', 'proc', '(', 'car', 'items', ')', ')', '(', 'map', 'proc', '(', 'cdr', 'items', ')', ')',
                ')', ')', ')'])


def test_lambda():
    assert (_tokenizer.tokenize("(define double (lambda (x) (* 2 x)))") ==
            ['(', 'define', 'double', '(', 'lambda', '(', 'x', ')', '(', '*', 2, 'x', ')', ')', ')'])

    assert (_tokenizer.tokenize("(define compose (lambda (f g) (lambda (x) (f (g x)))))")
            == ['(', 'define', 'compose', '(', 'lambda', '(', 'f', 'g', ')', '(', 'lambda', '(', 'x', ')', '(', 'f',
                '(', 'g', 'x', ')', ')', ')', ')', ')'])


def test_let():
    assert _tokenizer.tokenize("(let ((x 2) (y 3)) (+ x y))") == ['(', 'let', '(', '(', 'x', 2, ')', '(', 'y', 3, ')',
                                                                  ')', '(', '+', 'x', 'y', ')', ')']
