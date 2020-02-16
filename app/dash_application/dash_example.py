"""Create a Dash app within a Flask app."""
from pathlib import Path
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import dash
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from sqlalchemy import func, and_
import dash_table.FormatTemplate as FormatTemplate
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from .layout import html_layout
from app.models import db, Transaction, Budget
from app.main.helpers import column_prep, table_prep, modal_prep, tag_prep, modal_table_prep, stack_fig, stack_prep, dt_range, rangeSlider, anyMonthStart, bubble_prep, budget_prep, budget_fig, net_fig
from .modals import modal_shell, budget_modal
from flask import current_app as app
import ast



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

    exclusions = ast.literal_eval(app.config.get("EXCLUDE_CAT"))
    print('Exclude: ', exclusions)
    print(type(exclusions[0]))

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
                    dbc.Button("Budgets", id="launch_budget_modal", color="success")
        ),
            html.Div(
                children=budget_modal(),
                id='edit_budget_container'
        ),
            html.Div(
                    rangeSlider('figure')
                    ),
            html.Div(
                children=get_datasets(),
                id='dash-container'
        ),
            html.Div(
                children=modal_shell(),
                id='modal-container'
        )
            ,
            dcc.Graph(
                id='budgetStack',
                figure=budget_fig(budget_prep())
            ),
            dcc.Graph(
                id='netStack',
                figure=net_fig(budget_prep())
            )
            ,
            dcc.Graph(
                id='Stack',
                figure=stack_fig(stack_prep('tag'))
            ),
            dcc.Graph(
                id='Bubble',
                figure=bubble_prep('tag', anyMonthStart(date.today()))
            )
            ])
# TAGGING
    @dash_app.callback(
        [Output('modal_table', 'children'),
        Output(component_id='modal', component_property='is_open'),
        Output(component_id='dash-container', component_property='children'),
        Output(component_id='alert', component_property='children'),
        Output(component_id='alert', component_property='is_open'),
        Output(component_id='modal-container', component_property='children'),
        Output(component_id='Bubble', component_property='figure')],
        [Input(component_id='trnsx_table', component_property='active_cell'),
         Input(component_id='tag-dropdown', component_property='value'),
         Input(component_id='tag-input', component_property='value'),
         Input(component_id='apply_tag', component_property='value'),
        Input(component_id='submit', component_property='n_clicks'),
        Input(component_id='close', component_property='n_clicks'),
        Input(component_id='range_slider', component_property='value'),
        Input(component_id='transaction_budget_dropdown', component_property='value')],
        # Input(component_id='input-group-dropdown-input', component_property='value'),
        # Input(component_id='check_list', component_property='value')],
        [State("modal", "is_open")]
        )
    def get_active_cell(active_cell, drop_down, tag_input, apply_tag, submit_button, close_button, slider, is_open, budget_id):
        exclusions = ast.literal_eval(app.config.get("EXCLUDE_CAT"))
        print('Active Cell: ', active_cell)
        print('Input Value: ', drop_down)
        print('Check List: ', tag_input)
        print('Check List: ', apply_tag)
        print('Is Open: ', is_open)
        print('Submit: ', submit_button)
        print('Close: ', close_button)
        print('Slider: ', slider)
        if slider == 0 and not active_cell:
            raise dash.exceptions.PreventUpdate
        if slider != 0 and not submit_button or close_button:
            print('slider: ', slider)
            data = rangeSlider('data')
            i = data[slider]['label']
            m = i.split('/')[0]
            y = i.split('/')[1]
            start = anyMonthStart("20%s-%s-25" % (y, m))
            end = (start + relativedelta(months=1)).strftime('%Y-%m-%d')
            tdf = pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(exclusions)).filter(Transaction.pending == False).filter(and_(Transaction.date <= end, Transaction.date > start)).statement,db.session.bind)
            print(tdf)
            frame = table_prep(tdf)
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
            # ******* modal table ** model open **** table * alert txt ** alrt open ***** modal data *** bubble chart****
            return dash.no_update, dash.no_update, arr, dash.no_update, dash.no_update, dash.no_update, bubble_prep('tag', anyMonthStart(start))

        if active_cell and not submit_button or close_button:
            print('Active Cell Callback')
            trnsx = pd.read_sql(db.session.query(Transaction).filter(Transaction.id == active_cell['row_id']).statement, db.session.bind)
            th, tb = modal_table_prep(trnsx)
            is_open = True

            # frame = table_prep(pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(app.config.get("EXCLUDE_CAT"))).statement, db.session.bind))
            # new_data = frame.to_dict("rows")
            # *** modal table *model open * table * alert txt ** alrt open ***** modal chldrn *** bubble chart****
            return th + tb, is_open, dash.no_update, dash.no_update, False, dash.no_update, dash.no_update

        elif active_cell and submit_button:
            print('Submit Callback')
            if tag_input:
                tag = tag_input
            elif drop_down:
                tag = drop_down
            if apply_tag == 'ALL':
                trnsx = db.session.query(Transaction).filter(Transaction.id == active_cell['row_id']).one()
                peers = db.session.query(Transaction).filter(Transaction.name == trnsx.name).update({'tag': tag, 'budget_id': budget_id})
                alrt = ('{} Tags Updated'.format(peers))
            elif apply_tag == 'ONE':
                trnsx = db.session.query(Transaction).filter(Transaction.id == active_cell['row_id']).update({'tag': tag})
                peers = db.session.query(Transaction).filter(Transaction.name == trnsx.name).update({'budget_id': budget_id})
                alrt = ('{} Tags Updated {} Budgets Updated'.format('One', peers))
            try:
                db.session.commit()
                print('Tag Updated')
            except:
                print('db error')
                db.session.rollback()
            is_open = False
            data = rangeSlider('data')
            i = data[slider]['label']
            m = i.split('/')[0]
            y = i.split('/')[1]
            start = anyMonthStart("20%s-%s-25" % (y, m))
            # *** modal table *model open * table * alert txt ** alrt open ***** modal chldrn *** bubble chart****
            return dash.no_update, is_open, get_datasets(), alrt, True, modal_shell(), bubble_prep('tag', anyMonthStart(start))

        elif active_cell and close_button:
            print('Close Callback')
            is_open = False
            alrt = 'No Updates'

            # *** modal table ****model open * table ******alert txt ** **alrt open ***** modal chldrn *** bubble chart****
            return dash.no_update, is_open, dash.no_update, dash.no_update, False, modal_shell(), dash.no_update



# BUDGET Maintenance
    @dash_app.callback(
        [Output(component_id='edit_budget_modal', component_property='is_open'),
        Output(component_id='budget_table', component_property='data')],
        [Input(component_id='launch_budget_modal', component_property='n_clicks_timestamp'),
        Input(component_id='budget_table', component_property='data_previous'),
        Input(component_id='budget_table', component_property='data_timestamp'),
         Input(component_id='new_budget_name', component_property='value'),
         Input(component_id='new_budget_amount', component_property='value'),
         Input(component_id='edit_budget_submit', component_property='n_clicks_timestamp'),
         Input(component_id='edit_budget_close', component_property='n_clicks')],
        [State("edit_budget_modal", "is_open"),
         State("budget_table", "data")]
        )
    def budget_maintenance(click_time, prev_table, prev_time, new_name, new_amount, submit, m_close, m_open, curr_data):
        # print('Budget Maintence Callback Initial Values')
        print('click_time: ', click_time)
        # print('Previous Data: ', prev_table)
        # print('Name Entered: ', new_name)
        # print('Amount Entered: ', new_amount)
        # print('Submit Button: ', submit)
        # print('Add Modal Close: ', m_close)
        # print('Add Modal Open: ', m_open)
        # print('Current Data: ', curr_data)

        if click_time is None:
            print('Budget Modal No Action')
            raise dash.exceptions.PreventUpdate
        elif datetime.fromtimestamp(click_time / 1000) > datetime.now() - timedelta(seconds=1):
            print('Modal Launch')
            return True, pd.read_sql(db.session.query(Budget).statement, db.session.bind).to_dict("rows")
        if new_amount and new_name and not submit:
            print('Typing...')
            return dash.no_update, dash.no_update
        elif new_amount and new_name and datetime.fromtimestamp(submit / 1000) < datetime.now() - timedelta(seconds=1):
            print('Typing...')
            return dash.no_update, dash.no_update
        elif new_name and new_amount and datetime.fromtimestamp(submit / 1000)> datetime.now() - timedelta(seconds=1):
            print('To Be Databased...')
            print('Current Data: ', curr_data)
            print('Name Entered: ', new_name)
            print('Amount Entered: ', new_amount)
            new_budget = Budget(name=new_name, amount=new_amount)
            db.session.add(new_budget)
            try:
                db.session.commit()
                print('New Budget Added')
            except:
                db.session.rollback()
                print('Error Adding Budget')
            return dash.no_update, pd.read_sql(db.session.query(Budget).statement, db.session.bind).to_dict("rows")

        if prev_table is not None and datetime.fromtimestamp(prev_time / 1000)> datetime.now() - timedelta(seconds=1):
            print("Table Changed, Deleting ROw")
            new = pd.DataFrame(curr_data)
            old = pd.DataFrame(prev_table)
            df = old.merge(new, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
            to_delete = df.to_dict("records")
            del_row = db.session.query(Budget).filter(Budget.id == to_delete[0]["id"]).one()
            db.session.delete(del_row)
            try:
                db.session.commit()
                print('Row Deleted')
            except:
                db.session.rollback()
                print('Error Deleting Row')

            return dash.no_update, pd.read_sql(db.session.query(Budget).statement, db.session.bind).to_dict("rows")

    return dash_app.server


def get_datasets():
    """Return previews of all CSVs saved in /data directory."""
    exclusions = ast.literal_eval(app.config.get("EXCLUDE_CAT"))
    data = pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(exclusions)).filter(Transaction.pending == False).filter(Transaction.date >= anyMonthStart(date.today())).statement, db.session.bind)
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





