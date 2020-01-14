"""Routes for core Flask app."""
from flask import Blueprint, render_template, current_app, request,  make_response
from app import db
from app.models import Transaction
from datetime import datetime as dt
from app.main import bp


@bp.route('/')
def home():
    """Landing page."""

    return render_template('index.html',
                           title='HawkAdmin',
                           template='home-template',
                           body=str(f"Test"))
