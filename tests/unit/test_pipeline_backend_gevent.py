import pytest

from imgrabber.pipeline.backend import GeventBackend
from imgrabber.register import task


@pytest.fixture
def gevent_back():
    return GeventBackend()


class TestGeventBackend(object):
    def test_run_tasks(self, gevent_back, mock):
        mock_func = mock()

        def test_func():
            mock_func()

        gevent_back.run(test_func)
        gevent_back.wait_until_complete()

        assert mock_func.called == True
