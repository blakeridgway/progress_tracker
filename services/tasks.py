from flask import request, render_template, redirect, url_for
from models.task import Task
from models.month import Month
from services.database import db

def tasks(app):
    @app.route("/month/<name>", methods=["GET", "POST"])
    def month(name):
        # Find the month
        month = Month.query.filter_by(name=name).first()

        # If the month doesn't exist, redirect to the index
        if not month:
            return redirect(url_for('index'))

        # Handle adding a new task if it's a POST request
        if request.method == "POST":
            description = request.form['description']
            new_task = Task(description=description, status="Not Started", month_id=month.id)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('month', name=name))

        # Fetch all tasks for this month
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
