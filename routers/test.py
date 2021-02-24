# from fastapi import APIRouter

# router = APIRouter()

# @router.get("/")
# async def read():
#     return 'hello from test'

from celery import Celery
from subprocess import run
app = Celery('tasks', broker='amqp://guest:guest@some-rabbit:5672//')
@app.task
def command(text):
    ret = run (["ls", "-al"])
    return ret