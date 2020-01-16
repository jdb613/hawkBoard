"""Create a Dash app within a Flask app."""
from pathlib import Path
import dash
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from sqlalchemy import func
import dash_table.FormatTemplate as FormatTemplate
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from .layout import html_layout
from app.models import db, Transaction
from app.main.helpers import column_prep, table_prep, bubble_prep, modal_prep, tag_prep, modal_table_prep
from flask import current_app as app



def Add_Dash(server):
    """Create a Dash app."""
    external_stylesheets = ['https://fonts.googleapis.com/css?family=Lato',
                            'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
                            dbc.themes.BOOTSTRAP
                        ]
    external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js']
    dash_app = dash.Dash(server=server,
                         external_stylesheets=external_stylesheets,
                         external_scripts=external_scripts,
                         routes_pathname_prefix='/dashapp/'
                         )

    # Override the underlying HTML template
    dash_app.index_string = html_layout
    # dash_app.css.config.serve_locally = True
    # dash_app.scripts.config.serve_locally = True
    # Create Dash Layout comprised of Data Tables
    dash_app.layout = html.Div(
        [   html.Hr(),
            dbc.Alert(
                "",
                id="alert",
                is_open=False,
                duration=4000,
            ),
            html.Hr(),
            html.Div(
                children=get_datasets(),
                id='dash-container'
        ),
            html.Div(
                children=modal_shell(),
                id='modal-container'
        )
            ])
    @dash_app.callback(
        [Output('modal_table', 'children'),
        Output(component_id='modal', component_property='is_open'),
        Output(component_id='dash-container', component_property='children'),
        Output(component_id='alert', component_property='children'),
        Output(component_id='alert', component_property='is_open'),
        Output(component_id='modal-container', component_property='children')],
        [Input(component_id='trnsx_table', component_property='active_cell'),
         Input(component_id='tag-dropdown', component_property='value'),
         Input(component_id='tag-input', component_property='value'),
         Input(component_id='apply_tag', component_property='value'),
        Input(component_id='submit', component_property='n_clicks'),
        Input(component_id='close', component_property='n_clicks')],
        # Input(component_id='input-group-dropdown-input', component_property='value'),
        # Input(component_id='check_list', component_property='value')],
        [State("modal", "is_open")]
        )
    def get_active_cell(active_cell, drop_down, tag_input, apply_tag, submit_button, close_button, is_open):
        print('Active Cell: ', active_cell)
        print('Input Value: ', drop_down)
        print('Check List: ', tag_input)
        print('Check List: ', apply_tag)
        print('Is Open: ', is_open)
        print('Submit: ', submit_button)
        print('Close: ', close_button)
        if not active_cell:
            print('No Cell Selection')
            raise dash.exceptions.PreventUpdate

        elif active_cell and not submit_button or close_button:
            print('Active Cell Callback')
            trnsx = pd.read_sql(db.session.query(Transaction).filter(Transaction.id == active_cell['row_id']).statement, db.session.bind)
            th, tb = modal_table_prep(trnsx)
            is_open = True

            # frame = table_prep(pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(app.config.get("EXCLUDE_CAT"))).statement, db.session.bind))
            # new_data = frame.to_dict("rows")
            return th + tb, is_open, dash.no_update, dash.no_update, False, dash.no_update

        elif active_cell and submit_button:
            print('Submit Callback')
            if tag_input:
                tag = tag_input
            elif drop_down:
                tag = drop_down
            if apply_tag == 'ALL':
                trnsx = db.session.query(Transaction).filter(Transaction.id == active_cell['row_id']).one()
                peers = db.session.query(Transaction).filter(Transaction.name == trnsx.name).update({'tag': tag})
                alrt = ('{} Tags Updated'.format(peers))
            elif apply_tag == 'ONE':
                trnsx = db.session.query(Transaction).filter(Transaction.id == active_cell['row_id']).update({'tag': tag})
                alrt = ('{} Tags Updated'.format('One'))
            try:
                db.session.commit()
                print('Tag Updated')
            except:
                print('db error')
                db.session.rollback()
            is_open = False
            # frame = table_prep(pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(app.config.get("EXCLUDE_CAT"))).statement, db.session.bind))
            # new_data = frame.to_dict("rows")
            return dash.no_update, is_open, get_datasets(), alrt, True, modal_shell()

        elif active_cell and close_button:
            print('Close Callback')
            is_open = False
            alrt = 'No Updates'
            # frame = table_prep(pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(app.config.get("EXCLUDE_CAT"))).statement, db.session.bind))
            # new_data = frame.to_dict("rows")
            return dash.no_update, is_open, dash.no_update, False, modal_shell()


    # @dash_app.callback(
    #     [Output(component_id='input-group-dropdown-input', component_property='value')],
    #     [Input(component_id='modal_drop', component_property='children')]
    # )
    # def add_selection(selection):
    #     if selection:
    #         print(selection)
    #         return selection
    #     else:
    #         raise dash.exceptions.PreventUpdate

    return dash_app.server


def get_datasets():
    """Return previews of all CSVs saved in /data directory."""
    data = pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(app.config.get("EXCLUDE_CAT"))).filter(Transaction.pending == False).statement, db.session.bind)
    frame = table_prep(data)
    arr = ['Transactions']
    table_preview = dash_table.DataTable(
        id='trnsx_table',
        columns=column_prep(frame.columns),
        data=frame.to_dict("rows"),
        row_selectable='single',
        sort_action="native",
        sort_mode='single',
        page_size= 50
    )
    arr.append(table_preview)
    return arr

def get_tags():
    tags = sorted([{"tag": t[0], "count": t[1]} for t in db.session.query(Transaction.tag, func.count(Transaction.id)).group_by(Transaction.tag).all() if t[0]], key=lambda k: k['count'], reverse=True)
    return [{"label": i['tag'] + " -" + str(i['count']), "value": i['tag']} for i in tags]

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


