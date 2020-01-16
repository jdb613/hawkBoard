import pandas as pd
import dash_table.FormatTemplate as FormatTemplate
from app import db
from app.models import Transaction
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash_html_components as html
from sqlalchemy import func
from flask import current_app as app
from datetime import datetime, timedelta, date


def anyMonthStart(todayDate):
#     todayDate = datetime.strptime(d, '%Y-%m-%d')
    if todayDate.day < 15 and todayDate.month == 1:
        start_year = todayDate.year -1
        month_start = str(start_year) + '-' + str(12) + '-' + str(15)
    elif todayDate.day < 15 and todayDate.month != 1:
        month_start = str(todayDate.year) + '-' + str(todayDate.month - 1) + '-' + str(15)
    else:
        month_start = str(todayDate.year) + '-' + str(todayDate.month) + '-' + str(15)
#     print('Start Date of Current Billing Period: ', datetime.strptime(month_start, '%Y-%m-%d').strftime('%m/%d/%y'))

    return datetime.strptime(month_start, '%Y-%m-%d')


def column_prep(cols):
  data = []
  for c in cols:
      if c == 'date':
          data.append({"name": c, "id": c, "type": "datetime"})
      elif c == 'amount':
          data.append({"name": c, "id": c,'type': 'numeric', 'format': FormatTemplate.money(0)})
      else:
          data.append({"name": c, "id": c})
  return data

def table_prep(frame):
  frame = frame.sort_values('date', ascending=False)
  frame['date'] = frame['date'].dt.strftime('%m/%d/%Y')
  new_frame = frame[['id', 'date', 'name', 'amount', 'account_id', 'category', 'sub_category', 'pending', 'tag']]
  new_frame['account_id'] = new_frame['account_id'].map({'LOgERxzqrNFLPZdyNx7oFb9JwX39wzU05vVvd': 'Chase', 'vqmBXOzaoOuxNRe533YbhrV4r0NqELCmZr5vX': 'Schwab'})

  return new_frame

def modal_prep(id):
  tags = db.session.query(Transaction.tag).distinct().all()
  return None

def modal_table_prep(t):
  table_header = [html.Thead(html.Tr([html.Th(""), html.Th("Tansaction Detail")]))]

  row1 = html.Tr([html.Td("ID"), html.Td(t.id)])
  row2 = html.Tr([html.Td("Date"), html.Td(t.date)])
  row3 = html.Tr([html.Td("Name"), html.Td(t.name)])
  row4 = html.Tr([html.Td("Amount"), html.Td(t.amount)])
  row5 = html.Tr([html.Td("Account"), html.Td(t.account_id)])
  row6 = html.Tr([html.Td("Category"), html.Td(t.category)])
  row7 = html.Tr([html.Td("Sub-Category"), html.Td(t.sub_category)])
  row8 = html.Tr([html.Td("Pending"), html.Td(str(t.pending))])

  table_body = [html.Tbody([row1, row2, row3, row4, row5, row6, row7, row8])]

  return table_header, table_body

def tag_prep():
  tags = db.session.query(Transaction.tag, func.count(Transaction.id)).group_by(Transaction.tag)
  badge_data = sorted([{"tag": t[0], "count": t[1]} for t in tags.all() if t[0]], key=lambda k: k['count'], reverse=True)
  dropdown_menu_items = []
  for b in badge_data:
    list_item = dbc.DropdownMenuItem(b["tag"] + " - " + str(b["count"]), id=str(b["tag"]))
    dropdown_menu_items.append(list_item)
  return dropdown_menu_items


def stack_prep(grp):
  tdf = pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(app.config.get("EXCLUDE_CAT"))).filter(Transaction.pending == False).statement,db.session.bind)
  dtindex = tdf.reset_index()
  dtindex['period'] = dtindex['date'].apply(lambda x: anyMonthStart(x))
  grouped = dtindex.groupby([dtindex['period'],grp]).sum().reset_index()
  pt = grouped.pivot_table(index=grp, columns='period', values='amount', fill_value=0)
  pt = pt.sort_index(axis='columns', level='period', ascending=False)
  return pt

def stack_fig(data):
  traces = [go.Bar(x=row.keys(),
             y=row.values,
             name=index)
      for index, row in data.iterrows()]

  stack_fig = go.Figure(data=traces, layout=go.Layout(title=go.layout.Title(text="Monthly Stack")))
  stack_fig.update_layout(barmode='stack', bargap=0.15, xaxis=dict(title='Date', tickangle=90, tickfont=dict(size=10), categoryorder='trace'
      ))

  return stack_fig

# dbc.Badge("Info", pill=True, color="info", className="mr-1")
# dbc.DropdownMenuItem("Deep thought", id="dropdown-menu-item-1"),
# dbc.DropdownMenuItem("Hal", id="dropdown-menu-item-2"),
# dbc.DropdownMenuItem(divider=True),
# dbc.DropdownMenuItem("Clear", id="dropdown-menu-item-clear")
