import re
from typing import Callable

TOKEN = str | None
TOKEN_VALUE = str | None | int | float | bool
NEXT_TOKEN_INDEX = int
TOKEN_EXTRACT_RULE = Callable[[TOKEN], TOKEN_VALUE]

# 数字
_NUMERAL_STARTS = set("0123456789") | set("-.")

# 合法标识符和操作符
_OP_SIGN = set("*/<=>+-")
_SYMBOL_CHARS = (_OP_SIGN |
                 _NUMERAL_STARTS |
                 set("_!?") |
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


def be_valid_symbol(text: str) -> bool:
    if len(text) == 0:
        return False

    for c in text:
        if c not in _SYMBOL_CHARS:
            return False

    return True


def be_comment_line(ch: str) -> bool:
    return _COMMENT == ch


_NUMBER_MATCH = re.compile(r"^-?[0-9]+(\.[0-9]+)?$")


def be_number_token(ch: list[str]) -> bool:
    if not ch:
        return False
    return _NUMBER_MATCH.match("".join(ch)) is not None


def be_whit_space_line(ch: str) -> bool:
    return ch in _WHITESPACE


def be_single_char_token(ch: str) -> bool:
    return ch in _SINGLE_CHAR_TOKENS


def be_boolean_prefix(ch: str) -> bool:
    return _BOOLEAN_PREFIX == ch


def be_not_token_end(ch: str) -> bool:
    return ch not in _TOKEN_END


def query_token_next_pos(cur_pos, line):
    token_end_pos = cur_pos

    while token_end_pos < len(line) and be_not_token_end(line[token_end_pos]):
        token_end_pos += 1

    return token_end_pos


def max_token_length_warning(token, length):
    if length > _MAX_TOKEN_LENGTH:
        import warnings
        warnings.warn("Token {} has exceeded the maximum token length {}".format(token, _MAX_TOKEN_LENGTH))
