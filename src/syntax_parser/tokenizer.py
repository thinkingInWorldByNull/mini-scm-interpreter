"""
 将文本转换成Token列表，有效Token为下面之一:

  * 数字：int or float
  * Bool: True or False
  * 符号: 字符串
  * 分隔符： 括号`()` 单引号`'`

注意：不含字符串类型
"""
from typing import Tuple, Callable

TOKEN = str | None
TOKEN_VALUE = str | None | int | float | bool
NEXT_TOKEN_INDEX = int
TOKEN_EXTRACT_RULE = Callable[[TOKEN], TOKEN_VALUE]

# 数字
_NUMERAL_STARTS = set("0123456789") | set(".")

# 合法标识符和操作符
_OP_SIGN = set("*/<=>+-")
_SYMBOL_CHARS = (_OP_SIGN |
                 _NUMERAL_STARTS |
                 set("!?") |
                 set("abcdefghijklmnopqrstuvwxyz") |
                 set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                 )

_WHITESPACE = set(" \t\n\r")
_SINGLE_CHAR_TOKENS = set("()'")

_TOKEN_END = _WHITESPACE | _SINGLE_CHAR_TOKENS
_DELIMITERS = _SINGLE_CHAR_TOKENS | {".", ","}

_MAX_TOKEN_LENGTH = 50
_COMMENT = ";"
_BOOLEAN_PREFIX = "#"


class Tokenizer:
    _TOKEN_TYPE_EXTRACT_RULE: list[TOKEN_EXTRACT_RULE] = [
        lambda token: token if token in _DELIMITERS else None,
        lambda token: True if token == "#t" or token == "true" else None,
        lambda token: False if token == "#f" or token == "false" else None,
        lambda token: token if token == "nil" else None,
        lambda token: _number_extract(token) if _be_number_token(token[0]) else None,
        lambda token: token.lower() if _be_valid_symbol(token) else None,
    ]

    def tokenize(self, line: str):
        return list(self._gen_token_stream(line))

    def _gen_token_stream(self, line: str):
        """解析token，丢弃空白文本和注释"""
        token, next_token_idx = _next_candidate_token(line, 0)

        while token:
            if (res := self._extract_token(token)) is not None:
                yield res
            else:
                _raise_token_value_exception(line, token, next_token_idx)
            token, next_token_idx = _next_candidate_token(line, next_token_idx)

    def _extract_token(self, token: TOKEN) -> TOKEN_VALUE:
        for rule in self._TOKEN_TYPE_EXTRACT_RULE:
            if (res := rule(token)) is None:
                continue
            return res


def _raise_token_value_exception(line: str, token: str, next_token_idx: int):
    error_message = [
        "warning: invalid token: {0}".format(token),
        " " * 4 + line,
        " " * (next_token_idx + 4) + "^"
    ]
    raise ValueError("\n".join(error_message))


def _number_extract(token: str):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            raise Exception(f"Expect number but find {token}")


def _next_candidate_token(line, k) -> Tuple[TOKEN, NEXT_TOKEN_INDEX]:
    while k < len(line):
        ch = line[k]

        if _be_comment_line(ch):
            return None, len(line)

        elif _be_whit_space_line(ch):
            k += 1

        elif _be_single_char_token(ch):
            return ch, k + 1

        elif _be_boolean_prefix(ch):  # 布尔值 #t or #f
            return line[k:k + 2], min(k + 2, len(line))

        else:
            j = _query_token_next_pos(k, line)
            _max_token_length_warning(line[k:j], min(j, len(line)) - k)

            return line[k:j], min(j, len(line))

    return None, len(line)


def _be_valid_symbol(text: str) -> bool:
    if len(text) == 0:
        return False

    for c in text:
        if c not in _SYMBOL_CHARS:
            return False

    return True


def _be_comment_line(ch: str) -> bool:
    return _COMMENT == ch


def _be_number_token(ch: str) -> bool:
    return ch in _NUMERAL_STARTS


def _be_whit_space_line(ch: str) -> bool:
    return ch in _WHITESPACE


def _be_single_char_token(ch: str) -> bool:
    return ch in _SINGLE_CHAR_TOKENS


def _be_boolean_prefix(ch: str) -> bool:
    return _BOOLEAN_PREFIX == ch


def _be_not_token_end(ch: str) -> bool:
    return ch not in _TOKEN_END


def _query_token_next_pos(cur_pos, line):
    token_end_pos = cur_pos

    while token_end_pos < len(line) and _be_not_token_end(line[token_end_pos]):
        token_end_pos += 1

    return token_end_pos


def _max_token_length_warning(token, length):
    if length > _MAX_TOKEN_LENGTH:
        import warnings
        warnings.warn("Token {} has exceeded the maximum token length {}".format(token, _MAX_TOKEN_LENGTH))
