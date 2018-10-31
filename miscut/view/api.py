from flask.views import View
from flask import Response, json, request
from ..model import db, Conference, Event, VideoFile, VideoSegment
from miscut import app

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
            return Response("no conference %s" % conf, mimetype="text/plain")

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


class ApiEvents(View):
    @check_api_token
    def dispatch_request(self, conf=None):
        return Response("ehlo %s" % conf, mimetype="text/plain")


class ApiEvent(View):
    @check_api_token
    def dispatch_request(self, conf=None, id=None):
        return Response("ehlo %s/%s" % (conf, id), mimetype="text/plain")

class ApiRenderingEvents(View):
    @check_api_token
    def dispatch_request(self, conf):
        conference = Conference.query.filter_by(code = conf).first()
        if conference is None:
            return Response("no conference %s" % conf, mimetype="text/plain")
        events = []
        for f in Event.query.filter_by(conference_id=conference.id, state='rendering'):
            events.append(f.id)
        return Response(json.dumps(events), mimetype="application/json")

class ApiRenderingEvent(View):
    @check_api_token
    def dispatch_request(self, conf=None, id=None):
        conference = Conference.query.filter_by(code = conf).first()
        if conference is None:
            return Response("no conference %s" % conf, mimetype="text/plain")
        if request.method == 'POST':
            values = request.get_json()

        event = Event.query.filter_by(conference_id=conference.id, id=id).first()
        return Response(json.dumps({'event_id': event.event_id, 'name': event.name, 'segments': event.dict_segments}), mimetype="application/json")

def register_views(app, url="/api/"):
    app.add_url_rule(url+'file/<conf>', view_func=ApiFile.as_view('apps_api_file'), methods=['GET','POST'])
    app.add_url_rule(url+'events/<conf>', view_func=ApiEvents.as_view('apps_api_events'), methods=['GET'])
    app.add_url_rule(url+'events/<conf>/<id>', view_func=ApiEvent.as_view('apps_api_event'), methods=['GET','POST'])
    app.add_url_rule(url+'rendering/<conf>', view_func=ApiRenderingEvents.as_view('apps_api_rendering'), methods=['GET'])
    app.add_url_rule(url+'rendering/<conf>/<id>', view_func=ApiRenderingEvent.as_view('apps_api_renderingevent'), methods=['GET','POST'])

