from celery import Celery

app = Celery('rengu', broker='redis://prajna')

@app.task
def add(x, y):
    return x + y
