from typing import Callable, Dict, Type, Any
from inspect import isclass


def get_class_name(obj: Any) -> str:
    if not isclass(obj):
        class_name = str(obj.__class__.__name__)
    else:
        class_name = obj.__name__
    return class_name


class Dependency[T]:
    def __init__(self, provider: Callable[[], T], _type: Type[T]) -> None:
        self.provider = provider
        class_name = get_class_name(_type)
        self.dependency_type = class_name


class Lazy:
    _type: Type

    def __init__(self, _type: Type) -> None:
        self._type = _type

    @property
    def type_name(self) -> str:
        return get_class_name(self._type)

