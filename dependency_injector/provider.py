from .dependency import Dependency, Lazy, get_class_name
from .exceptions import DuplicateDependencyError
from typing import Any, Type, List, Union
from inspect import getfullargspec
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Provider:
    attrs_added: List[str] = []


def register(*dependencies: Dependency):
    print(len(dependencies))
    for value in dependencies:
        attr_name = value.dependency_type
        if getattr(Provider, attr_name, False):
            raise DuplicateDependencyError(f"""The dependency of type {attr_name} already exists
            consider using a factory for this""")
        print(f"Registering {attr_name}...")
        setattr(Provider, attr_name, value)
        Provider.attrs_added.append(attr_name)


def reset():
    for attr in Provider.attrs_added:
        delattr(Provider, attr)
    Provider.attrs_added = []


def lazy[T](_type: Type[T]) -> T:
    return Lazy(_type) # type: ignore


def inject(func):
    def wrapper(*args, **kwargs):
        argspec = getfullargspec(func)
        for i, value in enumerate(argspec.defaults or ()):
            if argspec.args[i] in kwargs:
                # Makes sure that given kwargs are not overwritten with injection
                continue
            if isinstance(value, Lazy):
                class_name = value._type
                dependency = find_dependency(class_name)
                kwargs[argspec.args[i]] = dependency.provider()
        return func(*args, **kwargs)
    return wrapper


def find_dependency[T](_type: Union[Type[T], Any]) -> Dependency[T]:
    attr_name = get_class_name(_type)
    dependency = getattr(Provider, attr_name, None)
    if dependency and isinstance(dependency, Dependency):
        logger.info(dependency.dependency_type)
        logger.info(attr_name)
        if dependency.dependency_type == attr_name:
            return dependency
    raise Exception

