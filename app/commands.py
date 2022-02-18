""" app commands

CLI commands for Net API Backend
"""
import click
from flask.cli import with_appcontext
from app.api.seed_test_db import init_sql_db
from app.extensions import db


def register_commands(app):
    """
    Register CLI commands
    :param app: Flask app
    :return: None
    """
    @app.cli.command("init-db")
    @with_appcontext
    # pylint: disable=unused-variable
    def init_db():
        """ Initialize the database
        :return: None
        """
        db.create_all()
        click.echo("Initialized the database.")

    @app.cli.command("drop-db")
    @with_appcontext
    # pylint: disable=unused-variable
    def drop_db():
        """ Drop the database, then initialize it
        :return: None
        """
        db.drop_all()
        click.echo("Dropped the database.")

    @app.cli.command("seed-db")
    @click.option(
        "-d",
        "--drop",
        is_flag=True,
        help="Drop the database before seeding",
    )
    @with_appcontext
    # pylint: disable=unused-variable
    def seed_db(drop):
        """ Seed the database with test data
        :return: None
        """
        init_sql_db(drop)
        if drop:
            click.echo("Dropped the database.")
        click.echo("Seeded the database with test data.")
