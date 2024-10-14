import numbers

from src.syntax_parser.token_syntax_define import be_valid_symbol

_DELIMITERS = set("()'.")


def be_end(token: str) -> bool:
    return token == ")"


def be_start(token: str) -> bool:
    return token == "("


def be_nil(token: str) -> bool:
    return token == "nil"


def be_quote(token: str) -> bool:
    return "'" == token


def be_valid_token(text: str | bool | int | float) -> bool:
    if isinstance(text, bool):
        return True
    if isinstance(text, numbers.Number):
        return True

    return text not in _DELIMITERS and be_valid_symbol(text)
