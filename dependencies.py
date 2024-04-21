from dependency_injector.dependency import Dependency

class Provider:
    STRING_DEP = Dependency(lambda: "It works! ")
