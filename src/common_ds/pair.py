from typing import Any


class _Nil:
    def __init__(self):
        super().__init__()
        self.car = ''
        self.cdr = None

    def __len__(self):
        return 0

    def __str__(self):
        return "()"

    def __repr__(self):
        return "nil"

    def map(self, _fn):
        return self


nil = _Nil()


class Pair:
    def __init__(self, car: Any, cdr: Any = None):
        self.car = car
        self.cdr = cdr

    def __len__(self):
        n, rest = 1, self.cdr

        while rest is not None:
            n += 1
            rest = rest.cdr

        return n

    def __eq__(self, p):
        if not isinstance(p, Pair):
            return False

        return self.car == p.car and self.cdr == p.cdr

    def _be_has_next(self):
        return self.cdr is not None

    def __str__(self):
        s = "(" + repl_str(self.car)
        rest = self.cdr
        while rest is not None and rest != nil:
            s += " " + repl_str(rest.car)
            rest = rest.cdr
        return s + ")"

    def __repr__(self):
        return "Pair({0}, {1})".format(repr(self.car), repr(self.cdr))


def repl_str(val):
    """Should largely match string (`val`), except for booleans and undefined.
    """
    if val is True:
        return "#t"
    if val is False:
        return "#f"
    if val is None:
        return "undefined"
    if isinstance(val, str) and val and val[0] == "\"":
        return "\"" + repr(val[1:-1])[1:-1] + "\""
    return str(val)
