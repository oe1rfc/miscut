import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_admin.base import expose

from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand

# Create Flask application
app = Flask(__name__)

app.config.from_pyfile('config_defaults.py')

if(os.environ.get('CONFIG')):
    app.config.from_pyfile(os.environ.get('CONFIG'))
else:
    try:
        app.config.from_pyfile('/etc/miscut/config.py')
    except FileNotFoundError:
        app.config.from_pyfile('../config.py', silent=True)


from miscut import model, view
from miscut.model import db

user_datastore = SQLAlchemyUserDatastore(db, model.User, model.Role)
security = Security(app, user_datastore)
migrate = Migrate(app, db)

admin = flask_admin.Admin(
    app,
    'MisCut',
    base_template='my_master.html',
    template_mode='bootstrap3',
    index_view=flask_admin.AdminIndexView(
        name='Home',
        url='/'
    )
)

@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

admin.add_view(view.EventCutView(model.Event, db.session, name='Uncut Events', category='Cutter', endpoint="cutter"))
admin.add_view(view.FileAssignView(model.VideoFile, db.session, name='Unassigned Files', category='Cutter', endpoint="assignfiles"))

admin.add_view(view.AdminView(model.Event, db.session, category='Events', endpoint="events"))
admin.add_view(view.AdminView(model.Conference, db.session, category='Events', endpoint="conferences"))

admin.add_view(view.AdminFileView(model.VideoFile, db.session, category='Files', endpoint="files"))
admin.add_view(view.AdminSegmentView(model.VideoSegment, db.session, category='Files', endpoint="segments"))

admin.add_view(view.AdminView(model.User, db.session, category='System', endpoint="admin/users"))
admin.add_view(view.AdminView(model.Role, db.session, category='System', endpoint="admin/roles"))

from miscut.view.api import register_views as register_api_views

register_api_views(app)

from miscut import commands

#from .schema import schema, GraphQLView

#app.add_url_rule(
#    '/graphql',
#    view_func=GraphQLView.as_view(
#        'graphql',
#        schema=schema,
#        context={},
#        graphiql=True
#    )
#)
