"""
 将文本转换成Token列表，有效Token为下面之一:

  * 数字：int or float
  * Bool: True or False
  * 符号: 字符串
  * 分隔符： 括号`()` 单引号`'`

注意：不含字符串类型
"""
from typing import Tuple, Generator, Any

from src.syntax_parser.token_syntax_define import TOKEN_EXTRACT_RULE, _DELIMITERS, query_token_next_pos, \
    max_token_length_warning, be_boolean_prefix, be_single_char_token, be_whit_space_line, be_comment_line, TOKEN, \
    NEXT_TOKEN_INDEX, TOKEN_VALUE, be_number_token, be_valid_symbol


class Tokenizer:
    _TOKEN_TYPE_EXTRACT_RULE: list[TOKEN_EXTRACT_RULE] = [
        lambda token: token if token in _DELIMITERS else None,
        lambda token: True if token == "#t" or token == "true" else None,
        lambda token: False if token == "#f" or token == "false" else None,
        lambda token: token if token == "nil" else None,
        lambda token: _number_extract(token) if be_number_token(token) else None,
        lambda token: token.lower() if be_valid_symbol(token) else None,
    ]

    def tokenize(self, line: str) -> list[str]:
        return list(self._extract_token_stream(line))

    def _extract_token_stream(self, line: str):
        for token, next_token_idx in _mk_candidate_token_stream(line):
            if (res := self._extract_token(token)) is not None:
                yield res
            else:
                _raise_token_value_exception(line, token, next_token_idx)

    def _extract_token(self, token: TOKEN) -> TOKEN_VALUE:
        for rule in self._TOKEN_TYPE_EXTRACT_RULE:
            if (res := rule(token)) is None:
                continue
            return res


def _raise_token_value_exception(line: str, token: str, next_token_idx: int):
    error_message = [
        "error: invalid token: {0}".format(token),
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


def _mk_candidate_token_stream(line) -> Generator[Tuple[TOKEN, NEXT_TOKEN_INDEX], Any, None]:
    token, next_token_idx = _next_candidate_token(line, 0)

    while next_token_idx <= len(line) and token:
        yield token, next_token_idx
        token, next_token_idx = _next_candidate_token(line, next_token_idx)


def _next_candidate_token(line, k) -> Tuple[TOKEN, NEXT_TOKEN_INDEX]:
    while k < len(line):
        ch = line[k]

        if be_comment_line(ch):
            return None, len(line)

        elif be_whit_space_line(ch):
            k += 1

        elif be_single_char_token(ch):
            return ch, k + 1

        elif be_boolean_prefix(ch):  # 布尔值 #t or #f
            return line[k:k + 2], min(k + 2, len(line))

        else:
            j = query_token_next_pos(k, line)
            max_token_length_warning(line[k:j], min(j, len(line)) - k)

            return line[k:j], min(j, len(line))

    return None, len(line)
