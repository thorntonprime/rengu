import os
import getpass

from blitzdb import FileBackend, MongoBackend
from pymongo import MongoClient, ASCENDING, DESCENDING
import xapian

if getpass.getuser() in [ 'rengu', 'uwsgi' ]:
    RENGUPATH='/srv/rengu'

elif os.uname()[0] == 'Darwin':
    RENGUPATH = os.environ.get("HOME",".") + '/Projects/rengu'

else:
    RENGUPATH = os.environ.get("HOME",".") + '/projects/rengu'

# Database either local or remote
if os.environ.get("RENGU") == "local":
    DB = FileBackend(RENGUPATH + "/db")
    XDBPATH="file://" + RENGUPATH + "/db/xdb"

else:
    mongo_client = MongoClient('prajna')
    DB = MongoBackend(mongo_client.rengu)
    XDBPATH="tcp://prajna:3333"

# Celery Configuration
broker_url = 'redis://prajna'
result_backend = 'redis://prajna'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'America/Los_Angeles'
enable_utc = True

# Worldcat info
worldcat_USERNAME = "theoszi"
worldcat_PASSWORD = "Cheroke3@Inca"
WORLDCAT_BASEURL = "https://www.worldcat.org"

