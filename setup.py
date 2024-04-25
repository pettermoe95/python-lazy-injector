from setuptools import setup, find_packages

__version__ = "0.0.2"

setup(
    name="lazy-injector",
    version=__version__,
    description="Simple dependency injection package",
    author="Petter Elenius Moe",
    author_email="pettermoe9530@gmail.com",
    url="https://github.com/pettermoe95/python-lazy-injector/tree/main",
    packages=["lazy_injector"] + ["lazy_injector." + pkg for pkg in find_packages("lazy_injector_")]
)

