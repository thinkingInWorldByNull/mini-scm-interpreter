from typing import Any

from src.inner_ds.pair import Pair, nil, repl_str


class SyntaxTree:
    def __init__(self, first: Any, remain: Any):
        self._first = first
        self._remain = remain

    @classmethod
    def from_pair_parser(cls, pair: Pair):
        return _convert(pair)

    def first(self):
        return self._first

    def remain(self):
        return self._remain

    def map(self, fn):
        root = SyntaxTree(fn(self.first()), self.remain())

        temp_res: SyntaxTree = root

        while temp_res._be_has_next():
            temp_res.cdr = SyntaxTree(fn(temp_res.remain().first()), None)
            temp_res = temp_res.cdr

        return root

    def _be_has_next(self):
        return self._remain is not None

    def __str__(self):
        s = "(" + repl_str(self._first)

        rest = self._remain
        while rest is not None and rest != nil:
            s += " " + repl_str(rest._first)
            rest = rest._remain
        return s + ")"

    def __repr__(self):
        return "SyntaxTree({0}, {1})".format(repr(self.first()), repr(self.remain()))


def _convert(pair):
    if isinstance(pair, Pair):
        return SyntaxTree(_convert(pair.car), _convert(pair.cdr))

    return pair
