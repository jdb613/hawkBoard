"""Routes for core Flask app."""
from flask import Blueprint, render_template, current_app, request,  make_response, url_for, jsonify
from app import db
from app.models import Transaction, Budget
from datetime import datetime, timedelta, date
from app.main import bp
import requests
import pandas as pd
from sqlalchemy import func, Date, cast, desc, and_
from app.main.helpers import anyMonthStart, map_it

@bp.route('/')
def home():
    """Landing page."""

    return render_template('index.html',
                           title='HawkAdmin',
                           template='home-template')

@bp.route('/homepage_data', methods=['GET', 'POST'])
def homepage_data():
    response = {}
    if request.args.get('type', '') == 'loadup':
      print("Sending Data to Index on Load Up")
      budgets = db.session.query(Budget).count()
      no_tags = db.session.query(Transaction).filter(Transaction.date >= anyMonthStart(date.today())).filter(Transaction.tag == None).count()
      no_budgets = db.session.query(Transaction).filter(Transaction.date >= anyMonthStart(date.today())).order_by(desc(Transaction.date)).count()
      this_month = db.session.query(Transaction).filter(Transaction.date >= anyMonthStart(date.today())).order_by(desc(Transaction.date)).all()
      special = db.session.query(Transaction).filter(Transaction.date >= anyMonthStart(date.today())).filter(Transaction.amount > 150).order_by(desc(Transaction.date)).count()
      response["A"] = budgets
      response["B"] = no_tags
      response["C"] = map_it([t.to_dict() for t in this_month])
      response["D"] = no_budgets
      response["E"] = special
    elif request.args.get('type', '') == 'untagged':
      print("Sending Untagged Transactions to Table")
      no_tags = db.session.query(Transaction).filter(Transaction.tag == None).order_by(desc(Transaction.date))
      response["A"] = map_it([t.to_dict() for t in no_tags.all()])
    elif request.args.get('type', '') == 'unbudgeted':
      print("Sending Unbudgeted Transactions to Table")
      no_budget = db.session.query(Transaction).filter(Transaction.budget_id == None).order_by(desc(Transaction.date))
      response["A"] = map_it([t.to_dict() for t in no_budget.all()])
    elif request.args.get('type', '') == 'special':
      print("Sending Special Transactions to Table")
      spec = db.session.query(Transaction).filter(Transaction.amount > 150).order_by(desc(Transaction.date))
      response["A"] = map_it([t.to_dict() for t in spec.all()])
    return jsonify(response)

@bp.route('/transaction_edit', methods=['GET', 'POST'])
def transaction_edit():
  response = {}
  if request.args.get('action', '') == 'table_click':
    trnsx = db.session.query(Transaction).filter(Transaction.id == request.args.get('id', '')).first()
    response['A'] = trnsx.to_dict()
    tags = db.session.query(Transaction.tag, func.count(Transaction.id)).group_by(Transaction.tag)
    response['B'] = sorted([{"tag": t[0], "count": t[1]} for t in tags.all() if t[0] is not None], key=lambda k: k['count'], reverse=True)
    budgets = db.session.query(Budget.name, func.count(Budget.id)).group_by(Budget.id)
    response['C'] = sorted([{"Budget": t[0], "count": t[1]} for t in budgets.all() if t[0] is not None], key=lambda k: k['count'], reverse=True)

  elif request.args.get('action', '') == 'update':
    print('Updated Transaction Data from Modal :', request.args)
    data = request.args.to_dict()
    response = {}
    if data['tag'] and data['tag_all'] == 'Yes':
      print('Tagging All with: ', data['tag'])
      trnsx = db.session.query(Transaction).filter(Transaction.id == data['id']).one()
      peers = db.session.query(Transaction).filter(Transaction.name == trnsx.name).update({'tag': data['tag']})
      response['A'] = ('{} Tags Updated'.format(peers))
    elif data['tag'] and data['tag_all'] == 'No':
      trnsx = db.session.query(Transaction).filter(Transaction.id == data['id']).update({'tag': data['tag']})
      response['A'] = ('{} Tags Updated'.format(trnsx))
    else:
      response['A'] = ('No Tags Updated')
    if data['budget'] and data['budget_all'] == 'Yes':
      print('Adding All to Budget: ', data['budget'])
      budge = db.session.query(Budget).filter(Budget.name == data['budget']).one()
      trnsx = db.session.query(Transaction).filter(Transaction.id == data['id']).one()
      peers = db.session.query(Transaction).filter(Transaction.name == trnsx.name).update({'budget_id': budge.id})
      response['B'] = ('{} Added to Budget'.format(peers))
    elif data['budget'] and data['budget_all'] == 'No':
      budge = db.session.query(Budget).filter(Budget.name == data['budget']).one()
      trnsx = db.session.query(Transaction).filter(Transaction.id == data['id']).update({'budget_id': budge.id})
      response['B'] = ('{} Added to Budget'.format(trnsx))
    else:
      response['B'] = ('No Budgets Updated')
    try:
        db.session.commit()
        print('db Updated')
    except:
        print('db error')
        db.session.rollback()

  return jsonify(response)

@bp.route('/budget_edit', methods=['GET', 'POST'])
def budget_edit():
  response = {}

  if request.args.get('action', '') == 'save':
    data = request.args.to_dict()
    print('Data Recieved: ')
    print(data)
    if not 'id' in data and not db.session.query(Budget).filter(Budget.name == data['name']).all():
      new_budget_item = Budget(name=data['name'], amount=data['amount'])
      try:
        db.session.add(new_budget_item)
        db.session.commit()
        response['A'] = ('New Budget {} added'.format(new_budget_item.name))
      except Exception as e:
        print(e)
        response['A'] = str(e)
    else:
      print('Existing Budget Detected')
      result = db.session.query(Budget).filter(Budget.id == int(data['id'])).update({'name': data['name'], 'amount': int(data['amount'])})
      try:
        db.session.commit()
        response['A'] = ('Budget {} updated'.format(result))
      except Exception as e:
        print(e)
        response['A'] = str(e)

  elif request.args.get('action', '') == 'edit':
    print("Edit Budget Clicked")
    data = request.args.to_dict()
    print('Data Recieved: ')
    print(data)
    budgets = db.session.query(Budget).all()
    response['A'] = [t.to_dict() for t in budgets]

  elif request.args.get('action', '') == 'delete':
    print('Deleting Budget {}'.format(request.args.get('id', '')))
    del_row = db.session.query(Budget).filter(Budget.id == request.args.get('id', '')).one()
    db.session.delete(del_row)
    try:
      db.session.commit()
      response['A'] = 'Row Deleted'
    except:
      db.session.rollback()
      response['A'] = 'Error Deleting Row'

  elif request.args.get('action', '') == 'view':
    print('Budget View Requested')
    test = db.session.query(Budget.name, Budget.amount, func.sum(Transaction.amount).label("total")).join(Transaction, Budget.transactions).filter(Transaction.date >= anyMonthStart(date.today())).group_by(Budget.name, Budget.amount)

    response["A"] = [r._asdict() for r in test.all()]
  return jsonify(response)
