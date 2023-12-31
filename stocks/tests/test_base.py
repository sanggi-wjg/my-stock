import pytest


@pytest.mark.django_db
class TestBase:
    pytestmark = pytest.mark.django_db

    @classmethod
    def setup_class(cls):
        # SETUP CLASS BASE
        pass

    @classmethod
    def teardown_class(cls):
        # TEAR DOWN CLASS BASE
        pass
