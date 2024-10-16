from src.inner_ds.pair import Pair, nil
from src.syntax_parser.parser_syntax_define import be_valid_token, be_nil, be_start, be_quote, be_end


class Parser:

    def parse(self, token_stream: list[str]):
        return _Parser(token_stream).expr()


class _Parser:
    def __init__(self, token_stream: list[str]):
        super().__init__()
        self.token_stream = token_stream

    def expr(self):
        return self._expr(self._take_left())

    def _expr(self, tok: str):
        # 遇到nil返回一个替代对象
        if be_nil(tok):
            return nil

        # 如果是普通符号或者解析好了的token比如True，false等直接返回
        elif be_valid_token(tok):
            return tok

        # 遇到起始符号返回rest
        elif be_start(tok):
            return self._rest(self._take_left())

        # 遇到引用比如【('Some (+ 1 2))】则构建一个Pair, 并重新对自身再次求表达式
        elif be_quote(tok):
            return Pair("quote", Pair(self._expr(self._take_left()), nil))

        # 其他符号或者不支持的特性先暂时抛异常提示
        raise SyntaxError("unexpected token: {0}".format(tok))

    def _rest(self, token: str):
        try:
            if be_end(token):
                return nil

            # 正常情况比如 【+ 1 2 3)】则直接求表达式和重新找rest部分
            return Pair(self._expr(token), self._rest(self._take_left()))
        except IndexError:
            raise SyntaxError(f"unexpected end of file, please check {token}")

    def _take_left(self):
        return self.token_stream.pop(0)
