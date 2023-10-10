from fastapi import FastAPI, Response, status
from data import users
from utils import user_model_abstraction, HTTP

app = FastAPI()


@app.get('/')
def get_root(response: Response):
    http = HTTP(response)
    return http.response(status.HTTP_200_OK, 'Hello World')


@app.get('/users')
def get_users(response: Response):
    http = HTTP(response)
    users_to_send = []
    for user in users:
        users_to_send.append(user_model_abstraction(user))
    return http.response(status.HTTP_200_OK, users_to_send)


@app.get('/users/{user_id}')
def get_user_by_id(user_id, response: Response):
    res = None
    http = HTTP(response)
    try:
        user_id = int(user_id)
        for user in users:
            if user['id'] == user_id:
                res = user_model_abstraction(user)
        if res is None:
            return http.response(status.HTTP_404_NOT_FOUND, res)
        return http.response(status.HTTP_200_OK, res)
    except ValueError:
        return http.response(status.HTTP_404_NOT_FOUND, 'Invalid user id')
    except Exception as e:
        return http.response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
