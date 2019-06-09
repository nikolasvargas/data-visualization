from collections import abc
from typing import Any, Callable
import time as _t
import functools


class FrozenData:
    """
    criado apenas para ler atributos de objetos do tipo dict ou JSON
    usando notação de atributos. Além de qualquerdict['attr']['attr'],
    você pode fazer qualquerdict.attr.attr para obter o valor
    """
    def __init__(self, mapping: Any) -> None:
        self._data = dict(mapping)

    def __getattr__(self, name: Any) -> Any:
        if hasattr(self._data, name):
            return getattr(self._data, name)
        else:
            return FrozenData.build(self._data[name])

    @classmethod
    def build(cls, obj: Any) -> Any:
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


def watch(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def wrapped(*args: Any, **kwargs: dict) -> Callable:
        start = _t.time()
        result = fn(*args, **kwargs)
        end = _t.time()
        fmt = "function: {}\nexec elapsed time: {}\n"
        print(fmt.format(fn.__name__, (end - start)))
        return result
    return wrapped
