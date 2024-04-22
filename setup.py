from setuptools import setup, find_packages

__version__ = "1.0.0"
setup(
    name="lazy-injector",
    description="Simple dependency injection package",
    author="Petter Elenius Moe",
    author_email="pettermoe9530@gmail.com",
    url="https://github.com/pettermoe95/python-lazy-injector/tree/main",
    packages=["lazy_injector"] + ["lazy_injector." + pkg for pkg in find_packages("lazy_injector_")]
)

