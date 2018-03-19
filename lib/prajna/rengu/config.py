import os
import getpass

if getpass.getuser() == 'rengu':
    RENGUPATH='/srv/rengu'

else:
    RENGUPATH = os.environ.get("HOME") + '/projects/rengu'

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
DB = FileBackend(RENGUPATH + "/db")

# Or MongoDB backend
#from pymongo import MongoClient, ASCENDING, DESCENDING
#from blitzdb import MongoBackend
#mongo_client = MongoClient('prajna')
#DB = MongoBackend(mongo_client.prajna.rengu)

# Worldcat info
worldcat_USERNAME = "theoszi"
worldcat_PASSWORD = "Cheroke3@Inca"
WORLDCAT_BASEURL = "https://www.worldcat.org"

XAPIANDB=RENGUPATH + "/db/xdb"
