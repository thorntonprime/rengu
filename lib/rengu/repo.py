# -*- coding: utf-8 -*-

from urllib.parse import urlparse
import os.path
from rengu.object import TYPES

class RepositoryException(Exception):
    """Exception raised for errors in reading the Rengu Repository.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class Repository(object):
    """Base class for all repositories

    Attributes:
        path -- Either a url to a repository or a file path
    """

    def __new__(cls, *args, **kwargs):

        if cls is Repository:

            if not args or not args[0]:
                return super(Repository, cls).__new__(RepositoryFile)

            else:
                url = urlparse(args[0])

                if url.scheme == 'file':
                    return super(Repository, cls).__new__(RepositoryFile)

                elif url.scheme == 'mongo':
                    return super(Repository, cls).__new__(RepositoryMongo)

                else:

                    if os.path.isdir(url.path):
                        return super(Repository, cls).__new__(RepositoryFile)
        
                    else:
                        raise RepositoryException("Invalid Repository URL")

class RepositoryFile(Repository):

    def __init__(self, path=None):
        import os

        if not path:
            self.path=os.environ.get("RENGUPATH")
            if not self.path:
                self.path=os.getcwd()
        else:
            url = urlparse(path)
            self.path = url.path

    def __str__(self):
        return(str(self.path))

    def check(self, verbosity=0):
        '''check
        Check the Rengu repository is set up correctly
        '''
        
        for t in TYPES:
            p = os.path.join(self.path, t + 's')     
            if verbosity > 1: yield "Checking " + t
            
            if os.path.isdir(p):
                 if verbosity > 1: yield p + " OK"
            else:
                yield "Error: " + p + " doesn't exist"

    def list_objects(self, objs, scopes=[]):
        
        if 'ANY' in scopes:
            scopes = TYPES

        for s in scopes:
            yield(s)

class RepositoryMongo(Repository):

    def __init__(self, path=None):
        url = urlparse(path)
        self.host = url.netloc
        self.database = url.path
        
    def __str__(self):
        return(str(self.host) + str(self.database))

    def check(self, verbosity=0):
        '''check
        Check the Rengu repository is set up correctly
        '''
        if verbosity > 1:
            yield("verbose mongo check")
        
    def list_objects(self, objs, scopes=[]):
        
        if 'ANY' in scopes:
            scopes = TYPES

        for s in scopes:
            yield(s)

