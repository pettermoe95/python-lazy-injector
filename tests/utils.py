from lazy_injector import reset


def set_up(func):
    def wrapper(*args, **kwargs):
        reset()
        return func(*args, **kwargs)
    return wrapper
