from typing import Tuple
from lazy_injector import Dependency, register, find_dependency, lazy, inject, get_class_name
from lazy_injector.exceptions import DuplicateDependencyError
from tests.utils import set_up
from pytest import raises



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


@set_up
def test_find_dependency():
    dep = Dependency(lambda: 456, int)
    register(dep)
    dep2 = find_dependency(int)
    assert dep == dep2


class MyTestClass():
    ...


def test_get_class_name():
    assert get_class_name(MyTestClass) == "MyTestClass"
    assert get_class_name(int) == "int"
    assert get_class_name(123) == "int"
    assert get_class_name(MyTestClass()) == "MyTestClass"



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



class MethodClass():

    @inject
    def inject_in_here(self, my_str: str = lazy(str)):
        return my_str

    @classmethod
    @inject
    def inject_class_method(cls, my_str: str = lazy(str)):
        return my_str

    @classmethod
    @inject
    def inject_class_method_many_args(cls, str_1: str, str_2: str, my_str: str = lazy(str), my_int: int = lazy(int), *args, **kwargs):
        return str_1, str_2, my_str, my_int

    @inject
    def inject_with_other_default(self, my_str: str = lazy(str), some_int = 0, my_int: int = lazy(int)):
        return my_str, some_int, my_int


@set_up
def test_inject_in_method():
    register(
        Dependency(dependency_provider, str),
        Dependency(lambda: 123, int)
    )
    method_class = MethodClass()
    assert method_class.inject_in_here() == dependency_provider()
    assert method_class.inject_class_method() == dependency_provider()

@set_up
def test_inject_with_pos_args():
    int_inject = 789
    register(
        Dependency(dependency_provider, str),
        Dependency(lambda: int_inject, int)
    )
    method_class = MethodClass()
    str_1, str_2, my_string, my_int = method_class.inject_class_method_many_args("str_1", "str_2", str_4="str_4")
    assert str_1 == "str_1"
    assert str_2 == "str_2"
    assert my_string == dependency_provider()
    assert my_int == int_inject


@set_up
def test_inject_with_other_default():
    int_inject = 789
    register(
        Dependency(dependency_provider, str),
        Dependency(lambda: int_inject, int)
    )
    method_class = MethodClass()
    my_str, some_int, my_int = method_class.inject_with_other_default()
    assert my_str == dependency_provider()
    assert some_int == 0
    assert my_int == int_inject

    my_str, some_int, my_int = method_class.inject_with_other_default(my_str="override", some_int=1)
    assert my_str == "override"
    assert some_int == 1
    assert my_int == int_inject



class InitInject:

    @inject
    def __init__(self, *, arg1, my_str: str = lazy(str)) -> None:
        self.arg1 = arg1
        self.my_str = my_str

    @inject
    def before_and_after(self, a, my_str: str = lazy(str), *, b, my_int: int = lazy(int)):
        return a, my_str, b, my_int


@set_up
def test_inject_into_init():
    register(
        Dependency(dependency_provider, str),
        Dependency(lambda: 7, int)
    )
    init_inject = InitInject(arg1=1)
    assert init_inject.my_str == dependency_provider()
    assert init_inject.arg1 == 1

    a, my_str, b, my_int = init_inject.before_and_after(a="a", b="b")
    assert a == "a"
    assert b == "b"
    assert my_str == dependency_provider()
    assert my_int == 7


    
