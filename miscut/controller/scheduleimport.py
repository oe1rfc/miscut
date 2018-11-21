from datetime import datetime, time
from dateutil import parser

from ..model import db, Conference, Event
import requests
import xml.etree.ElementTree as ET


class ScheduleImport():
    def __init__(self, conference):
        self.c = conference
        for k,e in self.fetch_events().items():
            self.update_event(e)
        db.session.commit()

    # taken from https://github.com/voc/auphonic-upload/blob/master/upload.py - thanks!
    # Download the Events-Schedule and parse all Events out of it. Yield a tupel for each Event
    def fetch_events(self):
        print('downloading pentabarf schedule')
        # destination list of events
        events = {}
        # download the schedule
        r = requests.get(self.c.scheduleurl)

        # check HTTP-Response-Code
        if r.status_code != 200:
            print('download failed')
            return events

        self.c.schedulexml = r.text.encode('utf-8')
        # parse into ElementTree
        schedule = ET.fromstring(r.text.encode('utf-8'))

        # iterate all days
        for day in schedule.iter('day'):
            # iterate all rooms
            for room in day.iter('room'):
                # iterate events on that day in this room
                for event in room.iter('event'):
                    # aggregate names of the persons holding this talk
                    personnames = []
                    for person in event.find('persons').iter('person'):
                        personnames.append(person.text)

                    # yield a tupel with the event-id, event-title and person-names
                    talkid = int(event.get('id'))
                    duration = 0
                    for d in event.find('duration').text.split(':'):
                        duration = duration*60 + int(d)

                    events[talkid] = {
                        'event_id': talkid,
                        'room': room.get('name'),
                        'room_id': ''.join((room.get('name').split())).lower(),
                        'title': event.find('title').text,
                        'subtitle': event.find('subtitle').text,
                        'date': parser.parse(event.find('date').text).replace(tzinfo=None),
                        'duration': duration,
                        'record': event.find('recording').find('optout').text != 'true',
                        'personnames': ', '.join(personnames)
                    }
        return events

    def update_event(self, data):
        event  = Event.query.filter_by(conference_id=self.c.id, event_id=data['event_id']).first()
        if event:
            desc_changed = False
            if event.name != data['title']:
                event.name = data['title']
                print("event title changed for '%s'." % event)
                desc_changed = True
            if event.subtitle != data['subtitle']:
                event.subtitle = data['subtitle']
                print("event subtitle changed for '%s'." % event)
                desc_changed = True
            if event.personnames != data['personnames']:
                event.personnames = data['personnames']
                print("event personnames changed for '%s'." % event)
                desc_changed = True
            if event.date != data['date']:
                event.date = data['date']
                print("event date changed for '%s'." % event)
            if event.duration != data['duration']:
                event.duration = data['duration']
                print("event duration changed for '%s'." % event)
            if event.room != data['room_id']:
                event.room = data['room_id']
                print("event room changed for '%s'." % event)
            if event.record != data['record']:
                event.record = data['record']
                print("event record changed for '%s'." % event)

            if desc_changed:
                event.description_updated = datetime.utcnow()

        else:
            event = Event(
                conference = self.c,
                event_id = data['event_id'],
                name = data['title'],
                subtitle = data['subtitle'],
                date = data['date'],
                duration = data['duration'],
                room = data['room_id'],
                record = data['record'],
                personnames = data['personnames']
            )
            db.session.add(event)
            print("new event '%s' created." % event)


