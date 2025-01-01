import os
from flask import Flask, render_template
from flask_login import LoginManager, current_user, login_required
from services.database import db
from services.auth import register
from services.tasks import tasks
from models.user import User
from models.task import Task
from models.month import Month

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()

# Register routes for auth and tasks
register(app)
tasks(app)

@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        tasks = Task.query.filter_by(user_id=current_user.id).all()
    else:
        tasks = []
    return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
