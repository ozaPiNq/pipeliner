import pytest
import six

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


@pytest.fixture
def mock():
    if six.PY2:
        from mock import MagicMock
    else:
        from unittest.mock import MagicMock

    return MagicMock
