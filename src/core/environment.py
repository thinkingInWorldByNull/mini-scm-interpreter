from typing import Any

from src.core.primitive_procedure import ProcedureError


class _Frame:

    def __init__(self, bindings: dict[str, Any]):
        self._bindings = bindings

    def be_exist(self, key: str) -> bool:
        return key in self._bindings

    def add_binding(self, key: str, value: Any):
        self._bindings[key] = value

    def get_val(self, key: str) -> Any:
        return self._bindings.get(key)

    @staticmethod
    def mk_empty_frame() -> "_Frame":
        return _Frame({})


class Environment:

    def __init__(self):
        super().__init__()

        self._frames: list[_Frame] = [_Frame.mk_empty_frame()]

    def lookup_variable_value(self, var_name: str) -> Any:
        for fm in self._frames:
            if fm.be_exist(var_name):
                return fm.get_val(var_name)

        raise ProcedureError(f"Unbound variable: {var_name}")

    def extend_environment(self, var_names: list[str], var_vals: list[Any]):
        new_env = Environment()

        new_env._frames = [_mk_frame(var_names, var_vals)] + self._frames

        return new_env

    def define_variable(self, var_name: str, var_val: Any):
        if self.first_frame().be_exist(var_name):
            raise ProcedureError(f"{var_name} duplicate define")

        self.set_variable(var_name, var_val)

    def set_variable(self, var_name: str, var_val: Any):
        self.first_frame().add_binding(var_name, var_val)

    def first_frame(self):
        return self._frames[0]


def _mk_frame(var_names: list[str], var_vals: list[Any]) -> _Frame:
    return _Frame(dict(zip(var_names, var_vals)))
