from app import db
from datetime import datetime

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
    transactions = db.relationship('Transaction', backref='budget', lazy='dynamic')

    def __repr__(self):
        return "<Transaction(name='%s', amount='%s')>" % (self.name, self.amount)
