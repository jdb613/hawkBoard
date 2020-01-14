"""Create a Dash app within a Flask app."""
from pathlib import Path
import dash
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
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
                            dbc.themes.BOOTSTRAP,
                            {
                                "href":"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
                                "rel":"stylesheet",
                                "integrity":"sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u",
                                "crossorigin":"anonymous"
                            }
                        ]
    external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js']
    dash_app = dash.Dash(server=server,
                         external_stylesheets=external_stylesheets,
                         external_scripts=external_scripts,
                         routes_pathname_prefix='/dashapp/')

    # Override the underlying HTML template
    dash_app.index_string = html_layout

    # Create Dash Layout comprised of Data Tables
    dash_app.layout = html.Div([html.Div(
        children=get_datasets(),
        id='dash-container'
      ),html.Div(
            children=modal_shell(),
            id='modal-container')])
    @dash_app.callback(
                        [Output('modal_table', 'children'), Output(component_id='modal', component_property='is_open'), Output("trnsx_table", "data")],
                        [Input(component_id='trnsx_table', component_property='active_cell'),
                         Input(component_id='submit', component_property='n_clicks'),
                         Input(component_id='close', component_property='n_clicks'),
                         Input(component_id='input-group-dropdown-input', component_property='value')],
                        [State("modal", "is_open")]
                        )
    def get_active_cell(active_cell, submit_button, close_button, input_value, is_open):
        data = pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(app.config.get("EXCLUDE_CAT"))).statement, db.session.bind)
        if not active_cell:
            raise PreventUpdate
        # print(active_cell)
        # print(is_open)
        # print(submit_button)
        # print(close_button)
        # print(input_value)
        elif active_cell and not submit_button or close_button:
            print('Active Cell Callback')
            trnsx = pd.read_sql(db.session.query(Transaction).filter(Transaction.id == active_cell['row_id']).statement, db.session.bind)

            th, tb = modal_table_prep(trnsx)
            is_open = True
            frame = table_prep(data)
            new_data = frame.to_dict("rows")
            return th + tb, is_open, new_data
        elif active_cell and submit_button:
            print('Submit Callback')
            print(input_value)
            print(active_cell)
            trnsx = db.session.query(Transaction).filter(Transaction.id == active_cell['row_id']).update({'tag': input_value})
            print(trnsx)
            # trnsx.tag = input_value
            # print(trnsx.tag)
            try:
                db.session.commit()
                print('Tag Updated')
            except:
                print('db error')
                db.session.rollback()
            is_open = False
            frame = table_prep(data)
            new_data = frame.to_dict("rows")
            return dash.no_update, is_open, new_data
        elif active_cell and close_button:
            print('Close Callback')
            is_open = False
            frame = table_prep(data)
            new_data = frame.to_dict("rows")
            return dash.no_update, is_open, new_data


    @dash_app.callback(
        [Output(component_id='input-group-dropdown-input', component_property='value')],
        [Input(component_id='modal_drop', component_property='children')]
    )
    def add_selection(selection):
        if not selection:
            raise PreventUpdate
        elif selection:
            print(selection)
            return selection

    # @dash_app.callback(
    #     [Output(component_id='modal', component_property='is_open')],
    #     [, Input(component_id='input-group-dropdown-input', component_property='value')],
    #     [State("modal", "is_open")]
    # )
    # def add_selection(sub_clicks, val, is_open):
    #     print(val)
    #     print(sub_clicks)
    #     print(is_open)
    #     is_open = False
    #     return is_open
    return dash_app.server



    # def toggle_modal(sclick, cclick, children, is_open):
    #     print('Toogle')
    #     if sclick:
    #         print(children)
    #         return not is_open
    #     elif cclick:
    #         return is_open
    # def toggle_modal(n1, n2, is_open):
    #     if n1 or n2:
    #         return not is_open
    #     return is_open

    # app.callback(
    #         Output("modal", "is_open"),
    #         [Input("submit", "n_clicks"), Input("close", "n_clicks")],
    #         [State("modal", "is_open")],
    #     )(toggle_modal)

    # @dash_app.callback(
    #     Output("modal", "is_open"),
    #     [Input("submit", "n_clicks"),Input("close", "n_clicks"), Input(component_id='modal', component_property='children')],
    #     [State("modal", "is_open")]
    # )

    # def toggle_modal(sclick, cclick, children, is_open):
    #     print('Toogle')
    #     if sclick:
    #         print(children)
    #         return not is_open
    #     elif cclick:
    #         return is_open

def get_datasets():
    """Return previews of all CSVs saved in /data directory."""
    data = pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(app.config.get("EXCLUDE_CAT"))).statement, db.session.bind)
    frame = table_prep(data)
    arr = ['This is an example Plot.ly Dash App.']
    table_preview = dash_table.DataTable(
        id='trnsx_table',
        columns=column_prep(frame.columns),
        data=frame.to_dict("rows"),
        row_selectable='single',
        sort_action="native",
        sort_mode='single'
    )
    arr.append(table_preview)
    return arr
def modal_shell():
    arr = []
    modal = dbc.Modal([
            dbc.ModalHeader("Transaction Tagging"),
            dbc.ModalBody(html.Div(
                [
                dbc.Table(id="modal_table", children=[], bordered=True),
                dbc.InputGroup(
                    [
                    dbc.DropdownMenu(id="modal_drop", children=[], label="Tags", addon_type="prepend"),
                    dbc.Input(id="input-group-dropdown-input", placeholder=""),
                    ]
                            ),
             ]
        )
    ),
            dbc.ModalFooter(
                [dbc.Button("Submit", id="submit", className="ml-auto"),
                dbc.Button("Close", id="close", className="ml-auto")]
                ),],
            id="modal",
            is_open=False)
    # modal = dbc.Modal(
    #      [
    #          dbc.ModalHeader("Your Header"),
    #          dbc.ModalBody("This is the content of the modal...file not XLS"),
    #          dbc.ModalFooter(
    #              dbc.Button("Close", id="close", className="ml-auto")
    #          ),
    #      ],
    #      id="modal",
    #      is_open=False,
    # )
    arr.append(modal)
    return arr


