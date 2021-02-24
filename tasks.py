from celery import Celery
from subprocess import run
app = Celery('tasks', broker='amqp://guest:guest@broker:5672//')
@app.task
def command(text):
    # ret = run (["ls", "-al"])
    ret = run (["touch", "output.txt"])
    f= open("output.txt","w+")
    f.write(text)
    f.close
    return ret