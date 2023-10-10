from fastapi import FastAPI
from data import users

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
        users_to_send.append({
            'id': user['id'],
            'name': user['name'],
            'username': user['username'],
            'email': user['email'],
        })
    return {
        'message': 'success',
        'data': users_to_send
    }
