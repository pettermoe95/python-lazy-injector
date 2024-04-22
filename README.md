# Introduction
Simple dependency injection framework for python

# Installation
Can be installed from pypi:
```sh
> pip install lazy-injector
```
# Usage
### Registering dependencies

```python
from lazy_injector import register, Dependency

class Foo:
    ...

def sample_provider():
    return Foo()


register(
    Dependency(lambda: "dependency", str),
    Dependency(sample_provider, Foo)
)
```
### Injecting dependencies
There are two functions to use, the `inject` and the `lazy`. The lazy must we used to get the dependency as a
default argument inside a function. I.e. `lazy(str)` will produce a placeholder default value that the laze_injector
can look for. The function needs to have the `@inject` set as a decorator, so that the lazy_injector
will replace the placeholder value with the actual dependency.

Here is an example:
```python
# Assuming class Foo has been registered
from lazy_injector import inject, lazy


@inject
def inject_foo(foo: Foo = lazy(Foo)):
    # Do stuff with foo
    foo.some_attr

```
