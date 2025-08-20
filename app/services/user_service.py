from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register_user(self, username, password, name=None):
        if self.repo.get_by_username(username):
            return None
        return self.repo.create(username, password, name)

    def authenticate(self, username, password):
        user = self.repo.get_by_username(username)
        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        return self.repo.get_by_id(user_id)
