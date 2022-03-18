from models import User


class UserRepository:
    model = User

    def auth(self, user_name, password):
        try:
            return self.model.select().where(
                (self.model.username == user_name) &
                (self.model.password == password)).dicts().get()
        except Exception as e:
            print(e)
            return None


