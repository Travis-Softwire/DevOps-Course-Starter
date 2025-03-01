from flask_login import current_user


def get_current_user_id():
    return current_user.get_id()
