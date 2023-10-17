from fastapi import FastAPI, Request, Response, status, Body
from fastapi.encoders import jsonable_encoder
from dotenv import dotenv_values
from pymongo import MongoClient
from bson.objectid import ObjectId
from utils import HTTP, task_model_abstraction
from models import Task

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
        task = request.app.database['tasks'].find_one({'_id': ObjectId(task_id)})
        task = task_model_abstraction(task)
        if len(task) == 0:
            return http.response(status.HTTP_404_NOT_FOUND, "No Task Found by this id")
        return http.response(status.HTTP_200_OK, task)
    except Exception as e:
        return http.response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@app.post('/tasks')
async def create_task(request: Request, response: Response, task: Task = Body(...)):
    http = HTTP(response)
    try:
        task = jsonable_encoder(task)
        new_task = request.app.database['tasks'].insert_one(task)
        created_task = request.app.database['tasks'].find_one({'_id': new_task.inserted_id})
        return http.response(status.HTTP_201_CREATED, task_model_abstraction(created_task))
    except Exception as e:
        return http.response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@app.on_event("startup")
def startup_db_client():
    try:
        app.mongodb_client = MongoClient(config["MONGODB_CONNECTION_URI"])
        app.database = app.mongodb_client[config["DB_NAME"]]
        print("Connected to the MongoDB database!")
    except Exception as e:
        print(f'Unable to connect with database: {str(e)}')
        exit(1)


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
