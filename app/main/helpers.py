import pandas as pd
import dash_table.FormatTemplate as FormatTemplate
from app import db
from app.models import Transaction, Budget
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_html_components as html
from sqlalchemy import func, and_
from flask import current_app as app
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import numpy as np
import re
import math
import ast
# from scipy import stats

def map_it(rez):
    out = []
    mapper = {"vqmBXOzaoOuxNRe533YbhrV4r0NqELCmZr5vX":"Schwab", "LOgERxzqrNFLPZdyNx7oFb9JwX39wzU05vVvd":"Chase" }
    for i in range(0, len(rez)):
        out.append({k: mapper.get(v, v) for k, v in rez[i].items()})
    return out


def dt_range(flag):
    exclusions = ast.literal_eval(app.config.get("EXCLUDE_CAT"))
    tdf = pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(exclusions)).filter(Transaction.pending == False).statement,db.session.bind)
    cur_date = tdf['date'].min().date()
    end = tdf['date'].max().date()
    marks = dict()
    count = 0
    while cur_date < end:
        marks.update({count:{'label': cur_date.strftime('%m/%y')}})
        # marks[count]:{'label': cur_date.strftime('%m/%y')}
        cur_date += relativedelta(months=1)
        count += 1
    if flag == 'list':
        print('marks: ', marks)
        return marks
    elif flag == 'end':
        print('end: ', count -1)
        return count -1

def rangeSlider(flag):
    exclusions = ast.literal_eval(app.config.get("EXCLUDE_CAT"))
    tdf = pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(exclusions)).filter(Transaction.pending == False).statement,db.session.bind)
    cur_date = tdf['date'].min().date()
    end = tdf['date'].max().date()
    marks = dict()
    count = 0
    while end > cur_date:
        marks.update({count:{'label': end.strftime('%m/%y')}})
        # marks[count]:{'label': cur_date.strftime('%m/%y')}
        end -= relativedelta(months=1)
        count += 1
    slider = dcc.Slider(
                    id="range_slider",
                    min=0,
                    max=count - 1,
                    value=0,
                    marks=marks
                )
    if flag == 'figure':
      return slider
    elif flag == 'data':
      return marks

def anyMonthStart(todayDate):
    if isinstance(todayDate, str):
      todayDate = datetime.strptime(todayDate, '%Y-%m-%d')
    if todayDate.day < 16 and todayDate.month == 1:
        start_year = todayDate.year -1
        month_start = str(start_year) + '-' + str(12) + '-' + str(16)
    elif todayDate.day < 16 and todayDate.month != 1:
        month_start = str(todayDate.year) + '-' + str(todayDate.month - 1) + '-' + str(16)
    else:
        month_start = str(todayDate.year) + '-' + str(todayDate.month) + '-' + str(16)
#     print('Start Date of Current Billing Period: ', datetime.strptime(month_start, '%Y-%m-%d').strftime('%m/%d/%y'))
    out = datetime.strptime(month_start, '%Y-%m-%d')
    # print('AnyMonth Result: ', out)
    return out


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
  # frame['date'] = frame['date'].dt.strftime('%m/%d/%Y')
  new_frame = frame[['id', 'date', 'name', 'amount', 'tag', 'category', 'sub_category', 'pending', 'account_id']]
  new_frame['account_id'] = new_frame['account_id'].map({'LOgERxzqrNFLPZdyNx7oFb9JwX39wzU05vVvd': 'Chase', 'vqmBXOzaoOuxNRe533YbhrV4r0NqELCmZr5vX': 'Schwab'})

  return new_frame

def budget_columns(cols):
  data = []
  for c in cols:
      if c == 'amount':
          data.append({"name": c, "id": c,'type': 'numeric', 'format': FormatTemplate.money(0)})
      else:
          data.append({"name": c, "id": c})
  data.append({'deletable': True})
  return data

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

def budget_prep():
  sumz = [{"budget_id":row[0], "sum":row[1]} for row in db.session.query(Transaction.budget_id, func.sum(Transaction.amount)).filter(Transaction.date >= anyMonthStart(date.today())).group_by(Transaction.budget_id).all()]
  keyz = [{"budget_id":row[0], "name":row[1], "amount":row[2]} for row in db.session.query(Budget.id, Budget.name, Budget.amount).distinct().all()]
  for k in keyz:
    for s in sumz:
        if k['budget_id'] == s['budget_id']:
            k['sum'] = s['sum']
            k['net'] = k['amount'] - k['sum']
  return pd.DataFrame(keyz)

def budget_fig(data):
  fig = go.Figure()
  fig.add_trace(go.Bar(x=data.name.to_list(),
                  y=data.sum.to_list(),
                  name='Current Progress'
                  ))
  fig.add_trace(go.Bar(x=data.name.to_list(),
                  y=data.amount.to_list(),
                  name='Budgeted'
                  ))
  fig.update_layout(
        title='Budget Progress',
        xaxis=dict(
            title='Budget',
            tickangle=90,
            tickfont=dict(
            size=8)
        ),
        yaxis=dict(
            title='Amount'
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group'
    )
  fig.update_yaxes(automargin=True)
  return fig

def net_fig(data):
  fig = go.Figure()
  fig.add_trace(go.Bar(x=data.name.to_list(), y=[x if x < 0 else 0 for x in data.net.to_list()],
                base=[x * -1  if x < 0 else 0 for x in data.net.to_list()],
                marker_color='crimson',
                name='Net'))
  fig.add_trace(go.Bar(x=data.name.to_list(),
                       y=[x for x in data.net.to_list() if x > 0],
                base=0,
                marker_color='lightslategrey',
                name='Net'
                ))
  return fig

def stack_prep(grp):
  exclusions = ast.literal_eval(app.config.get("EXCLUDE_CAT"))
  tdf = pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(exclusions)).filter(Transaction.pending == False).statement,db.session.bind)
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
  stack_fig.update_layout(barmode='stack', bargap=0.15, xaxis=dict(title='Date', tickangle=90, tickfont=dict(size=10), categoryorder='trace'))

  return stack_fig

def bubble_prep(grp, start):
  exclusions = ast.literal_eval(app.config.get("EXCLUDE_CAT"))
  print('Bubble Prep')
  end = start + relativedelta(months=1)
  print(start, end)
  data = pd.read_sql(db.session.query(Transaction).filter(~Transaction.category_id.in_(exclusions)).filter(Transaction.pending == False).filter(and_(Transaction.date < end.strftime('%Y-%m-%d'), Transaction.date >= start.strftime('%Y-%m-%d'))).statement, db.session.bind)
  tdf = data.set_index('date')
  print('Data Result: ', len(data))

  hover_text = []
  bubble_size = []

  for index, row in tdf.iterrows():
      hover_text.append((
                        'Name: {name}<br>'+
                        'Amount: {amount}<br>'+
                        'Category: {tag}<br>'+
                        'Sub-Category: {sub_category}<br>'+
                        'Account: {account_id}').format(
                                              name=row['name'],
                                              amount=row['amount'],
                                              tag=row['tag'],
                                              sub_category=row['sub_category'],
                                              account_id=row['account_id']))
      if row['amount'] < 0:
          bubble_size.append(math.sqrt(row['amount'] * -1))
      else:
          bubble_size.append(math.sqrt(row['amount']))

  tdf['text'] = hover_text
  tdf['size'] = bubble_size
  sizeref = 2.*max(tdf['size'])/(100**2)

  # Dictionary with dataframes for each continent
  categories = tdf['tag'].unique()
  category_data = {cat:tdf.query("tag == '%s'" %cat) for cat in categories}

  fig = go.Figure()

  for category_name, info in category_data.items():
      fig.add_trace(go.Scatter(
          x=info.index, y=info['tag'],
          name=category_name, text=info['text'],
          marker_size=info['size'],
          ))

  fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                                sizeref=sizeref, line_width=2))
  fig.update_layout(
      title='Transactions',
      xaxis=dict(
          title='Date',
          gridcolor='white',
          gridwidth=2,
      ),
      yaxis=dict(
          title='Amount',
          gridcolor='white',
          gridwidth=2,
      ),
      paper_bgcolor='rgb(243, 243, 243)',
      plot_bgcolor='rgb(243, 243, 243)',
  )
  return fig

# dbc.Badge("Info", pill=True, color="info", className="mr-1")
# dbc.DropdownMenuItem("Deep thought", id="dropdown-menu-item-1"),
# dbc.DropdownMenuItem("Hal", id="dropdown-menu-item-2"),
# dbc.DropdownMenuItem(divider=True),
# dbc.DropdownMenuItem("Clear", id="dropdown-menu-item-clear")
