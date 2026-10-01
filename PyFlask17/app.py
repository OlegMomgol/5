from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Task

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    category = request.args.get("category", "").strip()
    sort = request.args.get("sort", "").strip()

    query = Task.query

    if category:
        query = query.filter(Task.category == category)

    if sort == "done":
        query = query.order_by(Task.done.desc())
    elif sort == "undone":
        query = query.order_by(Task.done.asc())

    tasks = query.all()

    categories = [
        c[0] for c in db.session.query(Task.category).distinct().all() if c[0]
    ]

    total = Task.query.count()
    done_count = Task.query.filter_by(done=True).count()
    undone_count = total - done_count

    return render_template(
        "index.html",
        tasks=tasks,
        categories=categories,
        current_category=category,
        current_sort=sort,
        total=total,
        done_count=done_count,
        undone_count=undone_count,
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip() or "Общее"

        if not title:
            flash("Название задачи обязательно", "error")
            return redirect(url_for("add"))

        task = Task(title=title, description=description, category=category)
        db.session.add(task)
        db.session.commit()
        flash("Задача добавлена", "success")
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == "POST":
        task.title = request.form.get("title", "").strip()
        task.description = request.form.get("description", "").strip()
        task.category = request.form.get("category", "").strip() or "Общее"
        task.done = "done" in request.form

        if not task.title:
            flash("Название задачи обязательно", "error")
            return redirect(url_for("edit", task_id=task.id))

        db.session.commit()
        flash("Задача обновлена", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", task=task)


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Задача удалена", "success")
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle(task_id):
    task = Task.query.get_or_404(task_id)
    task.done = not task.done
    db.session.commit()
    return redirect(request.referrer or url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)