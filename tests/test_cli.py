"""
Test CLI commands
"""
import pytest


@pytest.mark.unittest
def test_init_db(app):
    """ Test init-db command
    """
    runner = app.test_cli_runner()
    result = runner.invoke(args=['init-db'])
    assert 'Initialized the database.' in result.output


@pytest.mark.unittest
def test_drop_db(app):
    """ Test drop-db command
    """
    runner = app.test_cli_runner()
    result = runner.invoke(args=['drop-db'])
    assert 'Dropped the database.' in result.output


@pytest.mark.unittest
def test_seed_db(app):
    """ Test seed-db command
    """
    runner = app.test_cli_runner()
    # We need to initialize the database first, before we can seed it
    result = runner.invoke(args=['init-db'])
    assert 'Initialized the database.' in result.output
    result = runner.invoke(args=['seed-db'])
    assert 'Seeded the database with test data.' in result.output


@pytest.mark.unittest
def test_seed_db_with_drop(app):
    """ Test seed-db -d command
    """
    runner = app.test_cli_runner()
    result = runner.invoke(args=['seed-db', '-d'])
    assert 'Dropped the database.' in result.output
    assert 'Seeded the database with test data.' in result.output
