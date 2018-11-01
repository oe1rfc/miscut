
from sqlalchemy.orm import validates
from datetime import datetime, date

from ..model import db

_event_states = db.Enum('stub', 'cutting', 'rendering', 'checking', 'published', '', 'source', 'problem', name='event_states')

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Unicode(16), nullable=False)
    name = db.Column(db.Unicode(64), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    scheduleurl = db.Column(db.Unicode(64), default=None)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    changed_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)
    comment = db.Column(db.UnicodeText, default="")

    def __str__(self):
        return self.code

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(_event_states, nullable=False, default='stub')
    conference_id = db.Column(db.Integer(), db.ForeignKey(Conference.id, ondelete="CASCADE"), nullable=False)
    conference = db.relationship(Conference, backref='events')
    event_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.UnicodeText, nullable=False)
    subtitle = db.Column(db.UnicodeText, default='')
    room = db.Column(db.Unicode(64), nullable=False)
    personnames = db.Column(db.UnicodeText, default=None)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    record = db.Column(db.Boolean(), nullable=False, default=True)
    date = db.Column(db.DateTime(), default=None)
    duration = db.Column(db.Integer, default=0)
    rendered_url = db.Column(db.Unicode(512), default=None)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    description_updated = db.Column(db.DateTime(), default=datetime.utcnow)
    changed_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=0)
    comment = db.Column(db.UnicodeText, default="")

    def __str__(self):
        return "%s/%s (%s)" % (self.conference.code, self.event_id, self.name)

    @property
    def segments(self):
        from .video import VideoSegment
        for segment in VideoSegment.query.filter_by(event_id=self.id, version=self.version):
            yield segment

    @property
    def dict_segments(self):
        segments = []
        for segment in self.segments:
            segments.append(segment.todict)
        return segments
