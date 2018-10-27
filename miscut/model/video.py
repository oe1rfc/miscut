
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint
from datetime import datetime, date

from ..model import db
from .event import Conference, Event

_video_types = db.Enum('footage', 'intro', 'outro', name='video_types')
_transition_types = db.Enum('cut', 'crossfade', name='transition_types')

class VideoFile(db.Model):
    __table_args__ = tuple(UniqueConstraint('storage_url', 'file_url', name='file_uniqe'))
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(_video_types, nullable=False, default='footage')
    conference_id = db.Column(db.Integer(), db.ForeignKey(Conference.id, ondelete="CASCADE"), nullable=False)
    conference = db.relationship(Conference, foreign_keys=conference_id, backref='files')
    active = db.Column(db.Boolean(), nullable=False, default=True)
    deleted = db.Column(db.Boolean(), nullable=False, default=False)
    startdate = db.Column(db.DateTime(), default=datetime.utcnow, nullable=True)
    length = db.Column(db.Numeric(precision=10, scale=2, decimal_return_scale=2), nullable=True)
    storage_url = db.Column(db.Unicode(256), nullable=False)
    file_url = db.Column(db.Unicode(256), nullable=False)
    comment = db.Column(db.UnicodeText, default="")

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    changed_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    @property
    def url(self):
        return "%s%s" % (self.storage_url, self.file_url)

    def __str__(self):
        return "%s (%s, %s)" % (self.file_url, self.conference.code, self.length)

    @property
    def todict(self):
        return {
                'id': self.id,
                'type': self.type,
                'storage_url': self.storage_url,
                'file_url': self.file_url,
                'conference': self.conference_id,
                'startdate': self.startdate,
                'length': float(self.length),
                'url': self.url
                }

class VideoSegment(db.Model):
    event_id = db.Column(db.Integer(), db.ForeignKey(Event.id, ondelete="CASCADE"), nullable=False, primary_key=True)
    event = db.relationship(Event, foreign_keys=event_id, backref='all_segments')

    videofile_id = db.Column(db.Integer(), db.ForeignKey(VideoFile.id, ondelete="CASCADE"), nullable=False)
    videofile = db.relationship(VideoFile, foreign_keys=videofile_id, backref='all_segments')

    segment_id = db.Column(db.Integer, primary_key=True, nullable=True)
    version = db.Column(db.Integer, primary_key=True, default=0)

    start = db.Column(db.Numeric(precision=10, scale=2, decimal_return_scale=2), nullable=False, default=0)
    length = db.Column(db.Numeric(precision=10, scale=2, decimal_return_scale=2), nullable=False)
    assigned = db.Column(db.Boolean(), nullable=False, default=False)

    transition = db.Column(_transition_types)
    transition_length = db.Column(db.Numeric(precision=10, scale=2, decimal_return_scale=2), default=None)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    changed_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    def __str__(self):
        return "%s Segment %d" % (self.event, self.segment_id)

    @validates('videofile', 'transition', 'transition_length')
    def validate_transition(self, key, value):
        print("K: %s    V:%s" % (key, value))
        if key == 'transition' and value is None:
            if self.videofile.type in ('intro', 'outro'):
                return 'crossfade'
            else:
                return 'cut'
        if key == 'transition_length':
            if self.transition is 'cut':
                return None
            if value is None and self.videofile.type in ('intro', 'outro'):
                return 1.00
        return value

    @property
    def todict(self):
        return {
                'event': self.event_id,
                'videofile': self.videofile.todict,
                'videofile_id': self.videofile_id,
                'segment_id': self.segment_id,
                'start': float(self.start),
                'length': float(self.length),
                'transition': self.transition,
                'transition_length': float(self.transition_length) if self.transition_length else None,
            }

