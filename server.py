from flask import Flask, render_template, request, redirect, url_for
from database import db, Task

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    months = db.session.query(Task.month_name).distinct().all()
    return render_template("index.html", months=months)

@app.route("/month/", methods=["GET", "POST"])
def redirect_to_month():
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            return redirect(url_for("index"))
        return redirect(url_for("month", name=name))

    name = request.args.get("name")
    if not name:
        return redirect(url_for("index"))
    return redirect(url_for("month", name=name))


@app.route("/month/<name>", methods=["GET", "POST"])
def month(name):
    print(f"Fetching tasks for month: {name}")  # Debugging line

    if request.method == "POST":
        description = request.form['description']
        new_task = Task(description=description, status="Not Started", month_name=name)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('month', name=name))

    tasks = Task.query.filter_by(month_name=name).all()
    print(f"Tasks fetched: {tasks}")  # Debugging line
    return render_template("month.html", month_name=name, tasks=tasks)

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
    tasks = Task.query.filter_by(month_name=month).all()
    for task in tasks:
        db.session.delete(task)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
