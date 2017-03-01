import pytest

from imgrabber.register import Register


@pytest.fixture(autouse=True)
def register():
    """ Return Register() instance and clear it on teardown """
    r = Register()
    yield r
    r._clear()


@pytest.fixture
def context():
    return {}
