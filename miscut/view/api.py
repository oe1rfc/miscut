from flask.views import View
from flask import Response, json, request
from ..model import db, Conference, Event, VideoFile, VideoSegment
from miscut import app
import xml.etree.ElementTree as ET

def check_api_token(func):
   def func_wrapper(*args, **kwargs):
        if request.headers.get('Authorization', None) is not app.config.get("API_TOKEN", None):
            return Response("API access not allowed."), 403
        return func(*args, **kwargs)
   return func_wrapper


class ApiFile(View):
    @check_api_token
    def dispatch_request(self, conf):
        conference = Conference.query.filter_by(code = conf).first()
        if conference is None:
            return Response("no conference %s" % conf, mimetype="text/plain"), 404

        if request.method == 'POST':
            values = request.get_json()

            new = VideoFile(
                conference = conference,
                type = values['type'],
                storage_url =  values['storage_url'],
                file_url = values['file_url'],
                length = values['length']
                )
            db.session.add(new)
            db.session.commit()
        files = []
        for f in VideoFile.query.filter(VideoFile.conference_id==conference.id):
            files.append(f.todict)
        return Response(json.dumps(files), mimetype="application/json")



class ApiFile(View):
    @check_api_token
    def dispatch_request(self, conf):
        conference = Conference.query.filter_by(code = conf).first()
        if conference is None:
            return Response("no conference %s" % conf, mimetype="text/plain"), 404

        if request.method == 'POST':
            values = request.get_json()

            videofile = VideoFile(
                conference = conference,
                type = values['type'],
                storage_url =  values['storage_url'],
                file_url = values['file_url'],
                length = values['length']
                )
            db.session.add(videofile)

            if 'event_id' in values:
                event = Event.query.filter_by(event_id = int(values['event_id']), conference_id = conference.id).first()
                if event:
                    self.add_to_event(conference, videofile, event)
            elif videofile.type == 'outro':
                self.add_outro(conference, videofile)

            db.session.commit()
        files = []
        for f in VideoFile.query.filter(VideoFile.conference_id==conference.id):
            files.append(f.todict)
        return Response(json.dumps(files), mimetype="application/json")

    def add_outro(self, conference, videofile):
        for e in conference.events:
            exists = False
            for s in e.segments:
                if s.videofile.type is 'outro':
                    exists = True
            if not exists:
                self.add_to_event(conference, videofile, e)

    def add_to_event(self, conference, videofile, event):
        if videofile.type == 'into':
            segment_id = 0
        else:
            segment_id = len(list(event.segments))
        segment = VideoSegment(
            event = event,
            videofile = videofile,
            segment_id = segment_id,
            start = 0,
            version = event.version,
            length = videofile.length
        )
        db.session.add(segment)



class ApiRenderingEvents(View):
    @check_api_token
    def dispatch_request(self, conf):
        conference = Conference.query.filter_by(code = conf).first()
        if conference is None:
            return Response("no conference %s" % conf, mimetype="text/plain"), 404
        events = []
        for f in Event.query.filter_by(conference_id=conference.id, state='rendering'):
            events.append(f.id)
        return Response(json.dumps(events), mimetype="application/json")

class ApiRenderingEvent(View):
    @check_api_token
    def dispatch_request(self, conf=None, id=None):
        conference = Conference.query.filter_by(code = conf).first()
        if conference is None:
            return Response("no conference %s" % conf, mimetype="text/plain"), 404
        event = Event.query.filter_by(conference_id=conference.id, id=id).first()

        if request.method == 'POST':
            values = request.get_json()
            if values and 'rendered_url' in values and event.state == 'rendering':
                event.rendered_url = values['rendered_url']
                event.state = 'checking'
                db.session.commit()
            else:
                return(400)

        return Response(json.dumps({'event_id': event.event_id, 'name': event.name, 'translation': event.translation, 'segments': event.dict_segments}), mimetype="application/json")


class ScheduleXMLexport(View):
    def dispatch_request(self, conf=None, id=None):
        conference = Conference.query.filter_by(code = conf).first()
        if conference is None:
            return Response("no conference %s" % conf, mimetype="text/plain"), 404
        try:
            schedule = ET.fromstring(conference.schedulexml)
            assert schedule is not None
        except:
            return Response("no schedule.xml for %s" % conf, mimetype="text/plain"), 404

        to_be_deleted = {}
        for room in schedule.iter('room'):
            for event in room.iter('event'):
                e = Event.query.filter_by(conference_id=conference.id, event_id=event.attrib['id']).first()
                if e and e.active == True and e.state == 'published' and e.rendered_url and e.record == True:
                    event.append(ET.Element('video_download_url'))
                    event.find('video_download_url').text = e.rendered_url
                else:
                    to_be_deleted[event] = room

        for event,room in to_be_deleted.items():
            room.remove(event)

        return Response(ET.tostring(schedule, encoding='utf-8', method='xml'), mimetype='text/xml; charset=utf-8')


def register_views(app, url="/api/"):
    app.add_url_rule(url+'file/<conf>', view_func=ApiFile.as_view('apps_api_file'), methods=['GET','POST'])
    app.add_url_rule(url+'rendering/<conf>', view_func=ApiRenderingEvents.as_view('apps_api_rendering'), methods=['GET'])
    app.add_url_rule(url+'rendering/<conf>/<id>', view_func=ApiRenderingEvent.as_view('apps_api_renderingevent'), methods=['GET','POST'])
    app.add_url_rule(url+'<conf>/schedule.xml', view_func=ScheduleXMLexport.as_view('apps_api_schedulexml'), methods=['GET'])

