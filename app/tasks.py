""" app tasks
Asynchronous tasks for the app
"""
from celery import Celery

celery = Celery('worker', autofinalize=False)
