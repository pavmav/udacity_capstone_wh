from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

class Warehouse(db.Model):
    __tablename__ = 'warehouses'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(120), nullable=False, unique=True)
    overdraft_control = db.Column(db.Boolean, default=False, nullable=False)
    balances = db.relationship('BalanceJournal', backref='warehouse')

    def __repr__(self) -> str:
        return f'<{self.name} (id:{self.id})>'

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'overdraft_control': self.overdraft_control
    }

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(120), nullable=False, unique=True)
    volume = db.Column(db.Integer, nullable=False, default=0)
    balances = db.relationship('BalanceJournal', backref='item')

    def __repr__(self) -> str:
        return f'<{self.name} (id:{self.id})>'

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'volume': self.volume
    }

class BalanceJournal(db.Model):
    __tablename__ = 'balance_journal'

    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), primary_key=True, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return f'<WH:{self.warehouse} I:{self.item} - quantity:{self.quantity})>'

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'warehouse': self.warehouse,
        'item': self.item,
        'quantity': self.quantity,
    }


