import functools

from todo_app.auth.current_todo_user import get_current_user_id
from todo_app.data.cosmos_user_repository import CosmosUserRepository
from flask_login import current_user
from flask import abort


def requires_role(role_names):
    def role_check_wrapper(func):
        @functools.wraps(func)
        def check_roles_and_execute(*args, **kwargs):
            cosmos_user_repository = CosmosUserRepository()
            for role_name in role_names:
                if cosmos_user_repository.does_user_have_role(get_current_user_id(), role_name):
                    return func(*args, **kwargs)
            abort(403)
        return check_roles_and_execute
    return role_check_wrapper

