from typing import Any

from src.common_ds.pair import Pair, repl_str, nil


class SyntaxTree:
    def __init__(self, first: Any, remain: Any):
        self._first = first
        self._remain = remain

    @classmethod
    def from_pair_parser(cls, pair: Pair):
        return _convert(pair)

    @staticmethod
    def be_nil(p):
        return p is None or p == nil

    @staticmethod
    def be_syntax_tree(p):
        return isinstance(p, SyntaxTree)

    @staticmethod
    def flat(tree: "SyntaxTree") -> list[str]:
        if SyntaxTree.be_nil(tree) or not SyntaxTree.be_syntax_tree(tree):
            return []

        return [tree.first()] + SyntaxTree.flat(tree.remain())

    def first(self):
        return self._first

    def remain(self):
        return self._remain

    def map(self, fn):
        if self.be_nil(self.remain()):
            return SyntaxTree(fn(self.first()), nil)

        return SyntaxTree(fn(self.first()), self.remain().map(fn))

    def _be_has_next(self):
        return self._remain is not None and not self.be_nil(self._remain)

    def __str__(self):
        s = "(" + repl_str(self._first)

        rest = self._remain
        while rest is not None and rest != nil:
            s += " " + repl_str(rest._first)
            rest = rest._remain
        return s + ")"

    def __repr__(self):
        return "SyntaxTree({0}, {1})".format(repr(self.first()), repr(self.remain()))

    def __len__(self):
        n, rest = 1, self.remain()

        while isinstance(rest, Pair):
            n += 1
            rest = rest.remain()

        if rest is not nil:
            raise TypeError("length attempted on improper list")
        return n

def _convert(pair):
    if isinstance(pair, Pair):
        return SyntaxTree(_convert(pair.car), _convert(pair.cdr))

    return pair
