from flask.views import View
from flask import Response, json, request
from ..model import db, Conference, VideoFile, VideoSegment
from miscut import app

def check_api_token(func):
   def func_wrapper(*args, **kwargs):
        if request.headers.get('Authorization', None) is not app.config.get("API_TOKEN", None):
            return Response("API access not allowed."), 403
        return func(*args, **kwargs)
   return func_wrapper


class RestFile(View):
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
        files = []
        for f in VideoFile.query.filter(VideoFile.conference_id==conference.id):
            files.append(f.todict)
        return Response(json.dumps(files), mimetype="application/json")


class RestEvents(View):
    @check_api_token
    def dispatch_request(self, conf=None):
        return Response("ehlo %s" % conf, mimetype="text/plain")


class RestEvent(View):
    @check_api_token
    def dispatch_request(self, conf=None, id=None):
        return Response("ehlo %s/%s" % (conf, id), mimetype="text/plain")

class RestPushFootage(View):
    @check_api_token
    def dispatch_request(self, conf=None, id=None):
        return Response("ehlo %s/%s" % (conf, id), mimetype="text/plain")

def register_views(app, url="/api/"):
    app.add_url_rule(url+'file/<conf>', view_func=RestFile.as_view('apps_api_file'), methods=['GET','POST'])
    app.add_url_rule(url+'events/<conf>', view_func=RestEvents.as_view('apps_api_events'), methods=['GET'])
    app.add_url_rule(url+'events/<conf>/<id>', view_func=RestEvent.as_view('apps_api_event'), methods=['GET','POST'])

