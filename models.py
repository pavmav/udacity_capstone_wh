from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Warehouse(db.Model):
    __tablename__ = 'warehouses'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f'<{self.name} (id:{self.id})>'

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f'<{self.name} (id:{self.id})>'

