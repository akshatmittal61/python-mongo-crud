import fastapi


def user_model_abstraction(user):
    return {
        'id': user['id'],
        'name': user['name'],
        'username': user['username'],
        'email': user['email'],
    }


class Response:
    response: fastapi.Response = {}
    status_code = 200

    def status(self, status_code: int = 200):
        if status_code == 200:
            self.response.status_code = fastapi.status.HTTP_200_OK
        elif status_code == 404:
            self.response.status_code = fastapi.status.HTTP_404_NOT_FOUND
        elif status_code == 500:
            self.response.status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            self.response.status_code = status_code

    def body(self, body: fastapi.responses.JSONResponse):
        self.response.body = body

    def __init__(self, response: fastapi.Response, status: int = 200):
        self.response = response
        self.status(status)


class HTTP:
    response = None

    def status(self, status: int = 200):
        # self.response = Response(status=status)
        self.response.status(status)

    def __init__(self, response: fastapi.Response):
        self.response = Response(response)
