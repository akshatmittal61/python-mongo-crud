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
    try:
        users_to_send = []
        for user in users:
            users_to_send.append(user_model_abstraction(user))
        return http.response(status.HTTP_200_OK, users_to_send)
    except Exception as e:
        return http.response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


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


@app.post('/users')
def add_user(name: str, username: str, email: str, website: str, response: Response):
    http = HTTP(response)
    try:
        if name is None or username is None or email is None:
            return http.response(status.HTTP_400_BAD_REQUEST, 'Please enter name, email and username')
        if username in [user['username'] for user in users]:
            return http.response(status.HTTP_409_CONFLICT, f'Username {username} already in use')
        if email in [user['email'] for user in users]:
            return http.response(status.HTTP_409_CONFLICT, f'Email {email} already in use')
        new_user = {
            'id': len(users) + 1,
            'name': name,
            'username': username,
            'email': email
        }
        if website is not None:
            new_user['website'] = website
        users.append(new_user)
        return http.response(status.HTTP_201_CREATED, 'New User added successfully')
    except Exception as e:
        return http.response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@app.patch('/users/{user_id}')
def update_user(user_id, data, response: Response):
    http = HTTP(response)
    try:
        user_id = int(user_id)
        data = eval(data)
        if user_id not in [user['id'] for user in users]:
            return http.response(status.HTTP_404_NOT_FOUND, 'User not found')
        if len(data) == 0:
            return http.response(status.HTTP_400_BAD_REQUEST, 'No details updated')
        for user in users:
            if user['id'] == user_id:
                for key in ['name', 'email', 'username']:
                    if key in data:
                        user[key] = data[key]
                break
        return http.response(status.HTTP_200_OK, {
            'message': 'User updated successfully',
            'user': [user for user in users if user_id == user['id']][0]
        })
    except ValueError:
        return http.response(status.HTTP_404_NOT_FOUND, 'Invalid user id')
    except Exception as e:
        return http.response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
