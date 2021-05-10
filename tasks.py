from celery import Celery
from subprocess import run #nosec
import requests
import json
app = Celery('tasks', broker='amqp://guest:guest@broker:5672//')
@app.task
def command(url):    
    ret = run (["touch", "output.txt"]) #nosec
    f= open("output.txt","w+")
    f.write(url)
    f.close
    return ret
    