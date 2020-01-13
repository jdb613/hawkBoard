"""Routes for core Flask app."""
from flask import Blueprint, render_template
from flask import current_app as app
from flask import request, render_template, make_response
from datetime import datetime as dt
from .models import db, Transaction


main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates')


@main_bp.route('/')
def home():
    """Landing page."""

    return render_template('index.html',
                           title='Plotly Flask Tutorial.',
                           template='home-template',
                           body=str(f"Test"))
