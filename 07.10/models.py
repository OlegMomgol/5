from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String(10), default='medium')
    is_done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def is_overdue(self):
        return not self.is_done and self.deadline < datetime.now()

    @property
    def is_today(self):
        if self.is_done:
            return False
        return self.deadline.date() == datetime.now().date()

    @property
    def is_this_week(self):
        if self.is_done:
            return False
        today = datetime.now().date()
        delta = (self.deadline.date() - today).days
        return 0 < delta <= 7