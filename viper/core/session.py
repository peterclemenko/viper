# This file is part of Viper - https://github.com/botherder/viper
# See the file 'LICENSE' for copying permission.

import time
import datetime

from viper.common.out import *
from viper.common.objects import File
from viper.core.database import Database

class Session(object):
    def __init__(self):
        self.id = None
        # This will be assigned with the File object of the file currently
        # being analyzed.
        self.file = None
        # Timestamp of the creation of the session.
        self.created_at = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

class Sessions(object):
    def __init__(self):
        self.current = None
        self.sessions = []
        # Store the results of the last "find" command.
        self.find = None

    def close(self):
        self.current = None

    def is_set(self):
        # Check if the session has been opened or not.
        if self.current:
            return True
        else:
            return False

    def switch(self, session):
        self.current = session
        print_info("Switched to session #{0} on {1}".format(self.current.id, self.current.file.path))

    def new(self, path):
        # TODO: sould replace an existing session if the file is the same
        # otherwise we will have multiple entries for the same file.

        session = Session()

        total = len(self.sessions)
        session.id = total + 1

        # Open a section on the given file.
        session.file = File(path)

        # Try to lookup the file in the database. If it is already present
        # we get file name and 
        row = Database().find(key='sha256', value=session.file.sha256)
        if row:
            session.file.name = row[0].name
            session.file.tags = ', '.join(tag.to_dict()['tag'] for tag in row[0].tag)

        self.sessions.append(session)
        self.current = session

        print_info("Session opened on {0}".format(path))

__sessions__ = Sessions()
