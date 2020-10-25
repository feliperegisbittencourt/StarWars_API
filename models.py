from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True
    
    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

class Planet(BaseModel):
    __tablename__ = 'planets'
    
    planetsid = db.Column(db.Integer, primary_key = True)
    planetname = db.Column(db.String(255), unique = True, nullable = False)
    planetclimate = db.Column(db.String(255), nullable = False)
    planetterrain = db.Column(db.String(255), nullable = False)
    films = db.Column(db.Integer, nullable = True)