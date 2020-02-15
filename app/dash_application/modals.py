import dash
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
from app.main.helpers import budget_columns
from .layout import html_layout
from app.models import db, Transaction, Budget
from sqlalchemy import func, and_

def get_tags():
    tags = sorted([{"tag": t[0], "count": t[1]} for t in db.session.query(Transaction.tag, func.count(Transaction.id)).group_by(Transaction.tag).all() if t[0]], key=lambda k: k['count'], reverse=True)
    return [{"label": i['tag'] + " -" + str(i['count']), "value": i['tag']} for i in tags]
def get_budgets():
    data = pd.read_sql(db.session.query(Budget).statement, db.session.bind)
    table_preview = dash_table.DataTable(
        id='budget_table',
        columns=budget_columns(data.columns),
        data=data.to_dict("rows"),
        editable=True,
        row_deletable=True,
        sort_action="native",
        sort_mode='single',
        page_size= 50
    )
    return [table_preview]

def modal_shell():
    arr = []
    modal = dbc.Modal([
            dbc.ModalHeader("Transaction Tagging"),
            dbc.ModalBody(html.Div(
                [
                dbc.Table(id="modal_table", children=[], bordered=True),
                dcc.Input(
                        id='tag-input',
                        placeholder='Enter a New Tag...',
                        type='text',
                        value=''
                    ),
                dcc.Dropdown(
                        id='tag-dropdown',
                        options=get_tags(),
                        value='Choose Tag'
                    ),
                dcc.Dropdown(
                        id='transaction_budget_dropdown',
                        options=get_budgets(),
                        value='Choose Tag'
                    ),
                dcc.Dropdown(
                        options=[
                            {'label': 'Apply to All', 'value': 'ALL'},
                            {'label': 'Apply to One', 'value': 'ONE'},
                        ],
                        value='ONE',
                        id='apply_tag'
                    )
                 ]
            )
    ),
            dbc.ModalFooter(
                [dbc.Button("Submit", id="submit", className="ml-auto"),
                dbc.Button("Close", id="close", className="ml-auto")]
                )],
            id="modal",
            centered=True,
            is_open=False)

    arr.append(modal)
    return arr

def budget_modal():
    arr = []
    modal = dbc.Modal([
            dbc.ModalHeader("Budget Item Maintenance"),
            dbc.ModalBody(html.Div(
                [
                html.Div(
                    children=get_budgets(),
                    id='edit_budget_table_container'
                        ),
                html.Hr(),
                dbc.InputGroup(
                            [
                                dbc.Input(placeholder="Budget Name", id="new_budget_name"),
                            ],
                            className="mb-3",
                        ),
                dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("$", addon_type="prepend"),
                            dbc.Input(placeholder="Amount", type="number", id="new_budget_amount"),
                            dbc.InputGroupAddon(".00", addon_type="append"),
                        ],
                        className="mb-3",
                    )
                 ]
            )
    ),
            dbc.ModalFooter(
                [dbc.Button("Add", id="edit_budget_submit", className="ml-auto"),
                dbc.Button("Close", id="edit_budget_close", className="ml-auto")]
                )],
            id="edit_budget_modal",
            centered=True,
            is_open=False)

    arr.append(modal)
    return arr


