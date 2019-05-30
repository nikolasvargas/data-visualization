from collections import abc
from typing import Any


class FrozenData:
    """
    criado apenas para ler atributos de objetos do tipo dict ou JSON
    usando notação de atributos
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
