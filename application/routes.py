"""Routes for core Flask app."""
from flask import Blueprint, render_template
from flask import current_app as app
from flask import request, render_template, make_response
from datetime import datetime as dt
from .models import db, Transaction


main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@main_bp.route('/')
def home():
    """Landing page."""
    new_t = Transaction(t_id='J9orRLz10puLDey1nve8tdLrEnyN8Yfb8My6J',
                        name='MORTON WILLIAMS EMRDL',
                        amount=28.73,
                        account_id='LOgERxzqrNFLPZdyNx7oFb9JwX39wzU05vVvd',
                        date=dt.strptime('2019-12-31', '%Y-%m-%d'),
                        category_id='19047000',
                        category='Shops',
                        sub_category='Supermarkets and Groceries',
                        pending=False,
                        pending_id='avenRAzdEOIZVEQ1pxEeSNw0rxaKjgCZv7Ky4')  # Create an instance of the User class
    db.session.add(new_t)  # Adds new User record to database
    db.session.commit()  # Commits all changes
    return render_template('index.html',
                           title='Plotly Flask Tutorial.',
                           template='home-template',
                           body=str(f"{new_t} successfully created!"))
