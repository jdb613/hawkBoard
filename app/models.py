from app import db
from datetime import datetime, timedelta, date

class Transaction(db.Model):
    """Model for Transactions."""

    __tablename__ = 'transaction'
    id = db.Column(db.Integer,
                   primary_key=True)
    t_id = db.Column(db.String(128),
                         index=False,
                         unique=True,
                         nullable=False)
    name = db.Column(db.String(128),
                      index=False,
                      unique=False,
                      nullable=False)
    amount = db.Column(db.Float,
                      index=False,
                      unique=False,
                      nullable=False)
    account_id = db.Column(db.String(128),
                      index=False,
                      unique=False,
                      nullable=False)
    date = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False)
    category_id = db.Column(db.String(128),
                      index=False,
                      unique=False,
                      nullable=True)
    category = db.Column(db.String(128),
                      index=False,
                      unique=False,
                      nullable=True)
    sub_category = db.Column(db.String(128),
                      index=False,
                      unique=False,
                      nullable=True)
    tag = db.Column(db.String(128),
                      index=False,
                      unique=False,
                      nullable=True)
    pending_id = db.Column(db.String(128),
                      index=False,
                      unique=False,
                      nullable=True)
    pending = db.Column(db.Boolean,
                      index=False,
                      unique=False,
                      nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'))


    def to_dict(self):
        data = {
            'id': self.id,
            't_id': self.t_id,
            'date': self.date.strftime('%m/%d/%y'),
            'amount': self.amount,
            'account_id': self.account_id,
            'category': self.category,
            'category_id': self.category_id,
            'sub_category': self.sub_category,
            'tag': self.tag,
            'pending_id': self.pending_id,
            'pending': self.pending,
            'budget_id': self.budget_id,
            'name': self.name
            }
        return data

    def from_dict(self, data, new_trnsx=False):
        for field in ['tag', 'budget_id']:
            if field in data:
                setattr(self, field, data[field])
        if new_trnsx:
            for field in ['t_id', 'date', 'amount', 'account_id', 'category', 'category_id', 'sub_category', 'tag', 'pending_id', 'pending', 'name', 'budget_id']:
                if field in data:
                    setattr(self, field, data[field])

    def __repr__(self):
        return "<Transaction(name='%s', amount='%s', date='%s', sub_category='%s')>" % (self.name, self.amount, self.date, self.sub_category)

class Budget(db.Model):
    """Model for Budgets."""

    __tablename__ = 'budget'
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(128),
                      index=False,
                      unique=False,
                      nullable=False)
    amount = db.Column(db.Float,
                      index=False,
                      unique=False,
                      nullable=False)
    transactions = db.relationship('Transaction', backref='mybudget', lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'amount': self.amount
            }
        return data

    def from_dict(self, data, new_budget=False):
        for field in ['name', 'amount']:
            if field in data:
                setattr(self, field, data[field])
        if new_trnsx:
            for field in ['name', 'amount']:
                if field in data:
                    setattr(self, field, data[field])
    def __repr__(self):
        return "<Transaction(name='%s', amount='%s')>" % (self.name, self.amount)
