from fastapi import FastAPI, Request, Response, status
from dotenv import dotenv_values
from pymongo import MongoClient
from utils import HTTP

config = dotenv_values(".env")
app = FastAPI()


@app.get('/')
def get_root(response: Response):
    http = HTTP(response)
    return http.response(status.HTTP_200_OK, 'Hello World')


@app.get('/tasks')
async def get_all_tasks(request: Request, response: Response):
    http = HTTP(response)
    try:
        tasks = list(request.app.database['tasks'].find())
        return http.response(status.HTTP_200_OK, tasks)
    except Exception as e:
        return http.response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@app.get('/tasks/{task_id}')
async def get_task_by_id(task_id: str, request: Request, response: Response):
    http = HTTP(response)
    try:
        task = dict(request.app.database['tasks'].find(id == task_id))
        if len(task) == 0:
            return http.response(status.HTTP_404_NOT_FOUND, "No Task Found by this id")
        return http.response(status.HTTP_200_OK, task)
    except Exception as e:
        return http.response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_CONNECTION_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
