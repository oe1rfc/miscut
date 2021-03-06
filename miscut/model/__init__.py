from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from flask_security import current_user

import miscut

db = SQLAlchemy(miscut.app)

def insert_set_created_c(mapper, connection, target):
    if(current_user.is_authenticated):
        target.created_c_id = current_user.id

from .user import User, Role
from .event import Conference, Event
from .video import VideoFile, VideoSegment
