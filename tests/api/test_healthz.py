"""
Testing health check operations
"""
from unittest import mock, TestCase
import pytest

from flask_healthz import HealthError

from app.api import healthz


class HealthCheckTest(TestCase):
    """ Health check tests
    """
    @pytest.mark.unittest
    def test_liveness(self):
        """  Liveliness checks
        """
        healthz.db = mock.MagicMock()
        healthz.liveness()
        healthz.db.session.execute.side_effect = ValueError(
            'Just a standard value error')

        try:
            healthz.liveness()
            self.fail('Should have raised exception')
        except HealthError:
            pass
