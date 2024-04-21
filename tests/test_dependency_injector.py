from typing import Tuple
from dependency_injector import Dependency, reset, register, find_dependency, lazy, inject
from dependency_injector.exceptions import DuplicateDependencyError
from pytest import raises

def set_up(func):
    def wrapper(*args, **kwargs):
        reset()
        return func(*args, **kwargs)
    return wrapper


def dependency_provider():
    return "it works"


@inject
def injection(my_string: str = lazy(str)):
    return my_string


@set_up
def test_injects_dependency():
    register(
        Dependency(dependency_provider, str),
        Dependency(lambda: 123, int)
    )
    assert dependency_provider() == injection()


@set_up
def test_raises_duplicate_error():
    with raises(DuplicateDependencyError) as err:
        register(
            Dependency(dependency_provider, str),
            Dependency(dependency_provider, str)
        )
        assert err.type is type(DuplicateDependencyError)



class MyClass:
    def __init__(self, a: str) -> None:
        self.a = a

    def some_string(self) -> str:
        return self.a


class MyIntClass:
    def __init__(self, a: int) -> None:
        self.a = a

    def some_int(self) -> int:
        return self.a


@inject
def my_func(my_class: MyClass = lazy(MyClass)) -> str:
    return my_class.some_string()


@inject
def my_func_multiple(my_class: MyClass = lazy(MyClass), my_int_class: MyIntClass = lazy(MyIntClass)) -> Tuple[MyClass, MyIntClass]:
    return my_class, my_int_class


@set_up
def test_inject_custom_classes():
    register(
        Dependency(lambda: MyClass("my_string"), MyClass),
        Dependency(lambda: MyIntClass(123), MyIntClass)
    )

    my_string = my_func()
    assert my_string == "my_string"


@set_up
def test_inject_multiple_dependencies():
    register(
        Dependency(lambda: MyClass("my_string"), MyClass),
        Dependency(lambda: MyIntClass(123), MyIntClass)
    )
    my_class, my_int_class = my_func_multiple()
    assert my_class.a == "my_string"
    assert my_int_class.a == 123


@set_up
def test_override_injection():
    register(
        Dependency(lambda: MyClass("my_string"), MyClass),
        Dependency(lambda: MyIntClass(123), MyIntClass)
    )
    override_string = "overrided"
    my_class, my_int_class = my_func_multiple(my_class=MyClass(override_string))
    assert my_class.a == override_string
    assert my_int_class.a == 123
    # Check that we can ovveride all arguments
    override_int = 321
    my_class, my_int_class = my_func_multiple(
        my_class=MyClass(override_string),
        my_int_class=MyIntClass(override_int)
    )
    assert my_class.a == override_string
    assert my_int_class.a == override_int
