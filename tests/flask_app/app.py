from lazy_injector import inject, lazy
from flask import Blueprint, Flask, make_response
from tests.flask_app.classes import FlaskTestClass


'''
Main entry point file for the service.
Exposes two endpoints for processing dims and facts.

The jobs are processed in the background and send a
response to a given callback url when completed.
'''

routes = Blueprint('app', __name__)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes)
    return app


@routes.route("/test_route", methods=["POST"], endpoint="example1")
@inject
def test_route(my_str: str = lazy(str)):
    return make_response(my_str, 200)


@routes.route("/test_class_route", methods=["POST"], endpoint="example2")
@inject
def test_class_route(flask_test_class: FlaskTestClass = lazy(FlaskTestClass)):
    return make_response(flask_test_class.some_string, 200)

app = create_app()

