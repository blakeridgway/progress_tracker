from sqlalchemy.orm import relationship
from database import db

class Month(db.Model):
    __tablename__ = 'months'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    tasks = relationship('Task', backref='month', cascade="all, delete-orphan")
