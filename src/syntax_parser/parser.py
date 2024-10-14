from src.inner_ds.pair import Pair, nil

_DELIMITERS = set("()'.")


class Parser:

    def parse(self, token_stream: list[str]):
        return _Parser(token_stream).expr()


class _Parser:
    def __init__(self, token_stream: list[str]):
        super().__init__()
        self.token_stream = token_stream

    def expr(self):
        tok = self.take_first()

        # 遇到nil返回一个替代对象
        if _be_nil(tok):
            return nil

        # 如果是普通符号直接返回
        elif _be_symbol(tok):
            return tok

        # 遇到起始符号返回rest
        elif _be_start(tok):
            return self.rest()

        # 遇到引用比如【('Some (+ 1 2))】则构建一个Pair, 并重新对自身再次求表达式
        elif _be_quote(tok):
            return Pair("quote", Pair(self.expr(), nil))

        # 其他符号或者不支持的特性先暂时抛异常提示
        raise SyntaxError("unexpected token: {0}".format(tok))

    def rest(self):
        # 解析达到末尾返回nil
        if _be_end(self.get_first()):
            self.take_first()
            return nil

        # 正常情况比如 【+ 1 2 3)】则直接求表达式和重新找rest部分
        return Pair(self.expr(), self.rest())

    def get_first(self):
        return self.token_stream[0]

    def take_first(self):
        return self.token_stream.pop(0)


def _be_no_more(token: str) -> bool:
    return token is None


def _be_end(token: str) -> bool:
    return token == ")"


def _be_start(token: str) -> bool:
    return token == "("


def _be_nil(token: str) -> bool:
    return token == "nil"


def _be_quote(token: str) -> bool:
    return "'" == token


def _be_symbol(token: str) -> bool:
    return token not in _DELIMITERS
