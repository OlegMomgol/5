from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), default="")
    done = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(100), default="Общее")

    def __repr__(self):
        return f"<Task {self.id}: {self.title}>"