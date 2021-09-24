from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Warehouse(db.Model):
    __tablename__ = 'warehouses'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(120), nullable=False, unique=True)
    overdraft_control = db.Column(db.Boolean, default=False, nullable=False)

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
        'name': self.name
    }

