from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, flash, request

from models import db, Task
from forms import TaskForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-change-me'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def group_tasks(tasks):
    now = datetime.now()
    today = now.date()
    week_later = today + timedelta(days=7)

    groups = {
        'overdue': [],
        'today': [],
        'week': [],
        'later': [],
        'done': [],
    }

    for t in tasks:
        if t.is_done:
            groups['done'].append(t)
        elif t.deadline < now:
            groups['overdue'].append(t)
        elif t.deadline.date() == today:
            groups['today'].append(t)
        elif t.deadline.date() <= week_later:
            groups['week'].append(t)
        else:
            groups['later'].append(t)

    for key in groups:
        groups[key].sort(key=lambda x: x.deadline)
    return groups

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.deadline.asc()).all()
    groups = group_tasks(tasks)
    total = len(tasks)
    done = sum(1 for t in tasks if t.is_done)
    return render_template('index.html', groups=groups, total=total, done=done)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data.strip(),
            description=form.description.data,
            deadline=form.deadline.data,
            priority=form.priority.data,
        )
        db.session.add(task)
        db.session.commit()
        flash('Задача добавлена', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, title='Новая задача')


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    form._is_edit = True

    if form.validate_on_submit():
        task.title = form.title.data.strip()
        task.description = form.description.data
        task.deadline = form.deadline.data
        task.priority = form.priority.data
        db.session.commit()
        flash('задача обновлена', 'success')
        return redirect(url_for('index'))

    return render_template('edit.html', form=form, title='редактировать задачу')


@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = not task.is_done
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('задача удалена', 'info')
    return redirect(url_for('index'))


@app.template_filter('format_dt')
def format_dt(value):
    if not value:
        return ''
    return value.strftime('%d.%m.%Y %H:%M')


@app.context_processor
def inject_now():
    return {'now': datetime.now()}


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)