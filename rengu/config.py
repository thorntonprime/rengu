
# Celery Configuration
broker_url = 'redis://prajna'
result_backend = 'redis://prajna'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'America/Los_Angeles'
enable_utc = True

# BlitzDB configuration file backend
from blitzdb import FileBackend
DB = FileBackend("./db")

# Or MongoDB backend
#from pymongo import MongoClient
#from blitzdb import MongoBackend
#mongo_client = MongoClient('prajna')
#DB = MongoBackend(mongo_client.rengu)

