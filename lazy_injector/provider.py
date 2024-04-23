from .dependency import Dependency, Lazy, get_class_name
from .exceptions import DuplicateDependencyError
from typing import Any, Dict, Type, List, Union
from inspect import FullArgSpec, getfullargspec
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Provider:
    attrs_added: List[str] = []


def register(*dependencies: Dependency):
    for value in dependencies:
        attr_name = value.dependency_type
        if getattr(Provider, attr_name, False):
            raise DuplicateDependencyError(f"""The dependency of type {attr_name} already exists
            consider using a factory for this""")
        setattr(Provider, attr_name, value)
        Provider.attrs_added.append(attr_name)


def reset():
    for attr in Provider.attrs_added:
        delattr(Provider, attr)
    Provider.attrs_added = []


def lazy[T](_type: Type[T]) -> T:
    return Lazy(_type) # type: ignore


def swap_lazy(argspec: FullArgSpec, lazy_index: int, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    for i, value in enumerate(argspec.defaults or ()):
        if argspec.args[lazy_index+i] in kwargs:
            # Makes sure that given kwargs are not overwritten with injection
            continue
        if isinstance(value, Lazy):
            kwargs[argspec.args[lazy_index+i]] = find_dependency(value._type).provider()
    # Checking if has kwonlyargs set and injects dependencies
    if argspec.kwonlydefaults:
        for key, value in argspec.kwonlydefaults.items():
            if isinstance(value, Lazy):
                kwargs[key] = find_dependency(value._type).provider()
    return kwargs



def inject(_callable):
    argspec = getfullargspec(_callable)
    lazy_index = len(argspec.args or ())-len(argspec.defaults or ()) # Start index of default args
    # method
    if len(argspec.args) > 0 and argspec.args[0] == "self":
        def method_wrapper(self, *args, **kwargs):
            kwargs = swap_lazy(argspec, lazy_index, kwargs)
            return _callable(self, *args, **kwargs)
        return method_wrapper
    # class method
    elif len(argspec.args) > 0 and argspec.args[0] == "cls":
        def class_method_wrapper(cls, *args, **kwargs):
            kwargs = swap_lazy(argspec, lazy_index, kwargs)
            return _callable(cls, *args, **kwargs)
        return class_method_wrapper
    # function
    else:
        def function_wrapper(*args, **kwargs):
            kwargs = swap_lazy(argspec, lazy_index, kwargs)
            return _callable(*args, **kwargs)
        return function_wrapper




def find_dependency[T](_type: Union[Type[T], Any]) -> Dependency[T]:
    attr_name = get_class_name(_type)
    dependency = getattr(Provider, attr_name, None)
    if dependency and isinstance(dependency, Dependency):
        if dependency.dependency_type == attr_name:
            return dependency
    raise Exception

