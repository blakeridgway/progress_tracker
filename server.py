import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.task import Task
from models.month import Month
from models.user import User
from database import db

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
        
        print(f"Attempting to register user: email={email}, username={username}")
        
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            print("Error: User already exists.")
            flash('Email or username already exists. Please choose another one.', 'danger')
            return redirect(url_for('register'))
        
        user = User(email=email, username=username)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            print(f"User {username} registered successfully!")
            
            flash('Your account has been created successfully! You can now log in.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            print(f"Error during registration: {str(e)}")
            flash(f'Error creating account: {str(e)}', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['username_or_email']
        password = request.form['password']
        
        user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()
        
        if user and user.check_password(password):
            random_cookie = secrets.token_hex(16)
            session['user_cookie'] = random_cookie
            
            login_user(user)
            
            flash("Logged in successfully!")
            return redirect(url_for('index'))
        
        flash("Invalid email/username or password.")
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_cookie', None)

    logout_user()

    flash("You have been logged out.", 'success')
    return redirect(url_for('index'))

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

@app.route("/update_task_status/<task_id>/<new_status>", methods=["POST"])
def update_task_status(task_id, new_status):
    task = Task.query.get(task_id)
    if task:
        task.status = new_status
        db.session.commit()
    return '', 200

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
