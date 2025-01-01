from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.task import Task
from models.month import Month
from models.user import User
from database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    months = Month.query.all()
    return render_template("index.html", months=months)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('login'))

@app.route("/month/", methods=["POST"])
def redirect_to_month():
    name = request.form.get("name")
    if name:
        return redirect(url_for("month", name=name))
    return redirect(url_for("index"))

@app.route("/month/<name>", methods=["GET", "POST"])
def month(name):
    month = Month.query.filter_by(name=name).first()

    if not month:
        return redirect(url_for('index'))

    if request.method == "POST":
        description = request.form['description']
        new_task = Task(description=description, status="Not Started", month_id=month.id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('month', name=name))

    tasks = Task.query.filter_by(month_id=month.id).all()
    return render_template("month.html", month_name=name, tasks=tasks)

@app.route("/add_month", methods=["POST"])
def add_month():
    name = request.form.get("name")
    if not name or Month.query.filter_by(name=name).first():
        return redirect(url_for('index'))
    new_month = Month(name=name)
    db.session.add(new_month)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/add_task/<name>", methods=["POST"])
def add_task(name):
    if request.method == "POST":
        description = request.form['description']
        new_task = Task(description=description, status="Not Started", month=name)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('month', name=name))

    tasks = Task.query.filter_by(month=name).all()
    return render_template("month.html", month=month)

@app.route("/update_task/<name>/<task_id>", methods=["POST"])
def update_task(name, task_id):
    task = Task.query.get(task_id)
    if task:
        task.status = request.form['status']
        db.session.commit()
    return redirect(url_for('month', name=name))

@app.route("/delete_task/<name>/<task_id>", methods=["POST"])
def delete_task(name, task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('month', name=name))

@app.route("/delete_month/<month>", methods=["POST"])
def delete_month_route(month):
    month_to_delete = Month.query.filter_by(name=month).first()
    if month_to_delete:
        db.session.delete(month_to_delete)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
