import os
import requests
from flask import abort, redirect, request
from urllib.parse import urljoin, urlencode

from flask_login import LoginManager, login_user

from todo_app.auth.user import User
from todo_app.data.cosmos_user_repository import CosmosUserRepository

login_manager = LoginManager()


@login_manager.unauthorized_handler
def unauthenticated():
    query_params = {
        'client_id': os.environ['GITHUB_CLIENT_ID'] or "",
        'redirect_uri': urljoin(request.base_url, "login/callback")
    }
    query = "?" + urlencode(query_params)
    auth_url = "https://github.com/login/oauth/authorize"
    auth_request = urljoin(auth_url, query)
    return redirect(auth_request)


@login_manager.user_loader
def load_user(user_id):
    cosmos_user_repository = CosmosUserRepository()
    user = cosmos_user_repository.get_user_from_id(user_id)
    return User(user.id, user.name, user.roles)


def login_callback_delegate():
    code = request.args.get("code")
    if code is not None:
        token_url = "https://github.com/login/oauth/access_token"
        form_data = {
            "client_id": os.environ["GITHUB_CLIENT_ID"],
            "client_secret": os.environ["GITHUB_CLIENT_SECRET"],
            "code": code,
            "redirect_uri": urljoin(request.base_url, "callback"),
        }
        headers = {
            "Accept": "application/json",
        }
        token_response = requests.post(token_url, form_data, None, headers=headers)
        token_body = token_response.json()
        access_token = token_body.get("access_token")
        if access_token is not None:
            headers["Authorization"] = f"Bearer {access_token}"
            user_info_response = requests.get("https://api.github.com/user", headers=headers)
            if user_info_response is not None:
                user_info_body = user_info_response.json()
                user_id = user_info_body.get("id")
                user_name = user_info_body.get("name")
                if user_id is not None:
                    cosmos_user_repository = CosmosUserRepository()
                    if len(cosmos_user_repository.get_users()) == 0:
                        user = User(user_id, user_name, ['Admin', 'Reader'])
                    else:
                        user = User(user_id, user_name, ['Reader'])
                    cosmos_user_repository.save_user(user)
                    login_user(user)
                    return redirect('/')
    abort(401)


def initialise_auth(app):
    login_manager.init_app(app)
