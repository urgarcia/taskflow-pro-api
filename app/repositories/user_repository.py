from app.models.user import User
from extensions import db

class UserRepository:
    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def get_by_id(self, user_id):
        return User.query.get(user_id)

    def create(self, username, password, name=None):
        user = User(username=username, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
