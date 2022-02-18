# pylint: disable=duplicate-code
""" net_api entrypoint_celery
Main entrypoint to serve up the scaffold Backend Celery instance
"""
from app import create_celery

celery = create_celery()
