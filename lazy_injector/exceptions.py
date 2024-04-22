"""
Exceptions that can happen during dependency injection
"""

class DuplicateDependencyError(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        self.msg = msg
        super().__init__(*args)

