from celery import Celery
from subprocess import run
import requests
import json
app = Celery('tasks', broker='amqp://guest:guest@broker:5672//')
@app.task
def command(url):
    # ret = run (["ls", "-al"])
    ret = run (["touch", "output.txt"])
    f= open("output.txt","w+")
    f.write(url)
    f.close
    return ret
    