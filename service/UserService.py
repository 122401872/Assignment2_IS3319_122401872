from dao.UserDao import UserDAO

class UserService:
    def __init__(self, db_name="users.db"):
        self.userDao = UserDAO(db_name=db_name)

    def get_all_users(self):
        """Retrieve all users from the database."""
        return self.userDao.get_all_users()

    def get_user_by_email(self, user_email):
        """Retrieve a user by their email from the database."""
        return self.userDao.get_user_by_email(user_email)
