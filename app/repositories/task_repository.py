from app.models.task import Task
from extensions import db

class TaskRepository:
    def get_all(self):
        return Task.query.all()

    def get_by_id(self, task_id):
        return Task.query.get(task_id)

    def create(self, title, description):
        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()
        return task

    def update(self, task, data):
        for key, value in data.items():
            setattr(task, key, value)
        db.session.commit()
        return task

    def delete(self, task):
        db.session.delete(task)
        db.session.commit()
