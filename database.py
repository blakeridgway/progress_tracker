from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="Not Started")
    month_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Task {self.description}>'
