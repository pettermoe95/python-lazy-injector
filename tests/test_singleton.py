from tests.utils import set_up
from lazy_injector import register, SingletonDependency, lazy, inject
import uuid


def random_provider() -> uuid.UUID:
    return uuid.uuid4()


@inject
def get_same_uuid_everytime(my_uuid: uuid.UUID = lazy(uuid.UUID)) -> uuid.UUID:
    return my_uuid


@set_up
def test_uses_singleton():
    register(
        SingletonDependency(random_provider, uuid.UUID)
    )
    assert get_same_uuid_everytime() == get_same_uuid_everytime()
    assert get_same_uuid_everytime() == get_same_uuid_everytime()
    assert get_same_uuid_everytime() == get_same_uuid_everytime()

