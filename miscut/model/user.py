from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import validates
from datetime import datetime

from ..model import db

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(32), unique=True)

    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    name = db.Column(db.Unicode(64), nullable=False, unique=True, index=True)
    email = db.Column(db.Unicode(64), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    changed_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)
    password = db.Column(db.Unicode(255))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users'))

    def __str__(self):
        return self.name
