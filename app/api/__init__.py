""" app.api __init__

API Blueprint for the Source Data API Backend
"""
from flask import Blueprint, redirect, render_template, url_for

api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/')
def index():
    """ The main index route
    :return: str
    """
    return render_template('index.html')


@api_bp.route('/dashboard')
def dashboard():
    """ The dashboard route
    :return: str
    """
    return render_template('index.html')


@api_bp.route('/login')
def login():
    """ The main index route
    :return: str
    """
    return redirect(url_for('.dashboard'))


@api_bp.route('/logout')
def logout():
    """ The main index route
    :return: str
    """
    return auth0.logout()
