from app.repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self):
        self.repo = TaskRepository()

    def list_tasks(self):
        return self.repo.get_all()

    def get_task(self, task_id):
        return self.repo.get_by_id(task_id)

    def create_task(self, title, description):
        return self.repo.create(title, description)

    def update_task(self, task_id, data):
        task = self.repo.get_by_id(task_id)
        if not task:
            return None
        return self.repo.update(task, data)

    def delete_task(self, task_id):
        task = self.repo.get_by_id(task_id)
        if not task:
            return False
        self.repo.delete(task)
        return True
