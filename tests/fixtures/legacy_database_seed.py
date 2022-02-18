import pytest
from sqlalchemy.orm import Session

from app import Foo 


@pytest.fixture(scope='function')
def legacy_database_seed(db_session: Session) -> None:
    """ Initialize the database with test data """

    # This is the original database seed logic that the original tests rely
    # on. Until legacy tests are updated to use fixtures, this fixture
    # will serve as a stop gap that rebuilds the database for each test using
    # the original seed data

    foo = Foo(name='Bar')
    db_session.add(foo)
    db_session.commit()
