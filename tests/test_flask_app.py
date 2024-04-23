from .flask_app.app import app
from lazy_injector import Dependency, register, reset
from .flask_app.classes import FlaskTestClass


def test_flask_route_decorator():
    reset()
    flask_route_str = "test_string"
    register(
        Dependency(lambda: flask_route_str, str),
        Dependency(lambda: 7, int)
    )
    test_app = app.test_client()
    response = test_app.post("/test_route")
    data = response.data.decode("utf-8")
    assert data == flask_route_str

def test_flas_route_inject_class():
    reset()
    flask_route_str = "some_test_string"
    register(
        Dependency(lambda: FlaskTestClass(flask_route_str), FlaskTestClass)
    )
    test_app = app.test_client()
    response = test_app.post("/test_class_route")
    data = response.data.decode("utf-8")
    assert data == flask_route_str

