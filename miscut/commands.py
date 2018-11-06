import click
from miscut import app, db, model, user_datastore
from flask_security.utils import encrypt_password

from miscut.controller import ScheduleImport

@app.cli.command()
def initdb():
    """Initialize the database."""
    db.create_all()
    click.echo('Init db')

    admin_role = model.Role(name='admin')
    db.session.add(admin_role)

    user_datastore.create_user(
        name='admin',
        email='admin',
        password=encrypt_password('admin'),
        roles=[admin_role]
    )

    db.session.commit()

@app.cli.command()
def sampledata():
    """Create database with sample data."""

    db.create_all()

    admin_role = model.Role(name='admin')
    db.session.add(admin_role)

    user_datastore.create_user(
        name='admin',
        email='admin',
        password=encrypt_password('admin'),
        roles=[admin_role]
    )

    conference = model.Conference(
        code = "test",
        name = "test Conference"
        )

    events = []

    events.append(model.Event(
        conference = conference,
        event_id = 1,
        state = 'stub',
        name = "Test Event 1",
        room = "room1"
        ))

    events.append(model.Event(
        conference = conference,
        event_id = 2,
        state = 'stub',
        name = "Test Event 2",
        room = "room1"
        ))

    files = []
    files.append(model.VideoFile(
        conference = conference,
        type = 'intro',
        storage_url = "http://localhost:5000/static/assets/demo/",
        file_url = "162.ts",
        length = 8.05
        ))
    files.append(model.VideoFile(
        conference = conference,
        type = 'outro',
        storage_url = "http://localhost:5000/static/assets/demo/",
        file_url = "outro.ts",
        length = 5.02
        ))
    files.append(model.VideoFile(
        conference = conference,
        storage_url = "http://localhost:5000/static/assets/demo/",
        file_url = "pw17-162.mp4",
        length = 2238.59
        ))

    segments = []
    segments.append(model.VideoSegment(
        event =events[0],
        videofile = files[0],
        segment_id = 0,
        start = 0,
        length = 8.05
        ))
    segments.append(model.VideoSegment(
        event =events[0],
        videofile = files[2],
        segment_id = 1,
        start = 10,
        length = 2200
        ))
    segments.append(model.VideoSegment(
        event =events[0],
        videofile = files[1],
        segment_id = 2,
        start = 0,
        length = 5.02
        ))

    db.session.add(conference)

    for event in events:
        db.session.add(event)
    for f in files:
        db.session.add(f)
    for s in segments:
        db.session.add(s)
    db.session.commit()

@app.cli.command()
def createpw18():
    """Create database with sample data."""

    db.create_all()

    admin_role = model.Role(name='admin')
    db.session.add(admin_role)

    user_datastore.create_user(
        name='admin',
        email='admin',
        password=encrypt_password('admin'),
        roles=[admin_role]
    )

    conference = model.Conference(
        code = "pw18",
        name = "PrivacyWeek 2018",
        scheduleurl = "https://conference.c3w.at/pw18/schedule/export/schedule.xml"
        )
    db.session.add(conference)
    db.session.commit()


@app.cli.command()
@click.option('--conference', '-c')
def updateschedule(conference):
    if not conference:
        click.echo('missing -c <conferenceid>')
        return
    conference=model.Conference.query.filter_by(code=conference).first()
    if conference is None:
        click.echo('no such conference.')
        return
    if not conference.scheduleurl:
        click.echo('conference %s has no schedule url.' % conference)
        return
    ScheduleImport(conference)

