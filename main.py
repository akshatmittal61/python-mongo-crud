from fastapi import FastAPI, Response, status
from data import users
from utils import user_model_abstraction, HTTP

app = FastAPI()


@app.get('/')
def get_root():
    return {
        'message': 'success',
        'data': 'Hello World'
    }


@app.get('/users')
def get_users():
    users_to_send = []
    for user in users:
        users_to_send.append(user_model_abstraction(user))
    return {
        'message': 'success',
        'data': users_to_send
    }


@app.get('/users/{user_id}')
def get_user_by_id(user_id, response: Response):
    res = None
    http = HTTP(response)
    for user in users:
        if str(user['id']) == user_id:
            res = user_model_abstraction(user)

    if res is None:
        http.status(status.HTTP_404_NOT_FOUND)

    return {
        'message': 'success',
        'data': res
    }
