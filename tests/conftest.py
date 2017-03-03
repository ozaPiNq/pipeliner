import pytest
import six

from pipeliner.register import Register
from pipeliner.context import Context


@pytest.fixture(autouse=True)
def register():
    """ Return Register() instance and clear it on teardown """
    r = Register()
    yield r
    r._clear()


@pytest.fixture
def context():
    return Context()


@pytest.fixture
def mock():
    if six.PY2:
        from mock import MagicMock
    else:
        from unittest.mock import MagicMock

    return MagicMock
