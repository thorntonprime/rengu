#!/usr/bin/python3

import os
os.environ["SCRIPT_NAME"] = ""

from wsgidav.property_manager import ShelvePropertyManager
from wsgidav.lock_storage import LockStorageShelve

from wsgidav.fs_dav_provider import FilesystemProvider 
from wsgidav.wsgidav_app import DEFAULT_CONFIG, WsgiDAVApp 

file_provider = FilesystemProvider('/data/work')

user_mapping = {}

def addUser(realmName, user, password, description, roles=[]):
    realmName = "/" + realmName.strip(r"\/")
    userDict = user_mapping.setdefault(realmName, {}).setdefault(user, {})
    userDict["password"] = password
    userDict["description"] = description
    userDict["roles"] = roles

addUser("", "thornton", "toaster", "")
addUser("", "tester", "secret", "")

config = DEFAULT_CONFIG.copy() 

config.update({ 
  "provider_mapping": {"/w": file_provider }, 
  "user_mapping": user_mapping, 
  "verbose": 3, 
  "enable_loggers": [], 
  "propsmanager": ShelvePropertyManager("/var/www/lock/prajna-work-props.shelve"),
  "locksmanager": LockStorageShelve("/var/www/lock/prajna-work-locks.shelve"), 
  "domaincontroller": None, 
}) 


application = WsgiDAVApp(config) 

if __name__ == '__main__':
  
  application.run(host='0.0.0.0', port=8000, debug=True)

