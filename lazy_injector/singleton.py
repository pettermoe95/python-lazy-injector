from lazy_injector.dependency import Dependency, get_class_name
from typing import Dict, Callable, Type


class SingletonNotFoundError(Exception):
    def __init__(self, msg: str = "Singleton not found", *args: object) -> None:
        self.msg = msg
        super().__init__(*args)


class SingletonRegistry:
    registry: Dict[str, object] = {}

    @classmethod
    def get_singleton[T](cls, _class: Type[T]) -> T:
        singleton = cls.registry.get(get_class_name(_class))
        if isinstance(singleton, _class):
            return singleton
        raise SingletonNotFoundError(f"Singleton of type {get_class_name(_class)} was not found.")

    @classmethod
    def register_singleton(cls, instance: object):
        cls.registry[get_class_name(instance)] = instance


class SingletonDependency[T](Dependency[T]):
    def __init__(self, provider: Callable[[], T], _type: Type[T]) -> None:
        singleton_provider = lambda: singleton(provider, _type)
        super().__init__(singleton_provider, _type)


def singleton[T](provider: Callable[[], T], _class: Type[T]) -> T:
    # Trying to get the singleton here
    try:
        return SingletonRegistry.get_singleton(_class)
    except SingletonNotFoundError:
        # If singleton is not found, call the provider to get instance
        instance = provider()
        # provider returned the instance, need to register it here
        SingletonRegistry.register_singleton(instance)
        return instance
