import application.foxnotdead.users as users

class App:
    @staticmethod
    def run() -> None:
        user_input = "w"
        user = users.User.get_user(1)
        state = user.GetState()
        state.process_input(user_input)
        #afteward print state actions

        state = user.GetState()
