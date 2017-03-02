import pytest

from pipeliner.pipeline.backend import GeventBackend
from pipeliner.register import task


@pytest.fixture
def gevent_back():
    return GeventBackend()


class TestGeventBackend(object):
    def test_run_tasks(self, gevent_back, mock):
        mock_func = mock()

        def test_func(p1, p2, p3):
            mock_func()

        gevent_back.run(test_func, 1, 2, 3)
        gevent_back.wait_until_complete()

        assert mock_func.called == True
