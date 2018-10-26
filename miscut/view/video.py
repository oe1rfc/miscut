
from flask_admin.base import expose

from flask import request, redirect, flash, abort, json, Response
from flask_admin.helpers import get_redirect_target
from flask_admin.babel import gettext

from sqlalchemy.sql.expression import func
from flask_admin.model.helpers import get_mdict_item_or_list

from ..view import LoginView
from ..model import db, VideoFile, VideoSegment


class EventCutView(LoginView):
    can_delete = False
    can_create = False
    can_view_details = False

    def create_view(self):
        pass
    def delete_view(self):
        pass
    def ajax_update(self):
        pass

    def get_query(self):
        return super(EventCutView, self).get_query().filter(self.model.state == 'cutting',
                                                                                                self.model.active == True)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.state == 'cutting',
                                                                                    self.model.active == True)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_edit:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        event = self.get_one(id)

        if event is None:
            flash(gettext('Event does not exist.'), 'error')
            return redirect(return_url)

        return self.render(template = 'event_cut.html',
                               event = event)

    @expose('/edit/segments', methods=('GET', 'POST'))
    def rest_segments(self):
        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(get_redirect_target() or self.get_url('.index_view'))

        event = self.get_one(id)

        if event is None:
            flash(gettext('Event does not exist.'), 'error')
            return redirect(return_url)
        if request.method == 'GET':
            version = get_mdict_item_or_list(request.args, 'version')
            return Response(json.dumps({
                    'version': event.version,
                    'comment': event.comment,
                    'segments': event.dict_segments,
                }), mimetype="application/json")

        if request.method == 'POST':
            saved = request.get_json()
            print(saved)
            newversion = (event.version + 1)
            print("new version:", newversion)
            segments = []
            for s in saved:
                print()
                print (s)
                videofile=VideoFile.query.filter_by(id=int(s['videofile_id'])).first()
                print("file", videofile)
                print()
                segments.append(VideoSegment(
                    segment_id = int(s['segment_id'])+1,
                    event = event,
                    videofile = videofile,
                    start = float(s['start']),
                    length = float(s['length']),
                    assigned = True,
                    transition = s['transition'],
                    transition_length = s['transition_length'] if 'transition_length' in s else None,
                    version = newversion,
                ))
                print(segments)
            event.version = newversion
            for s in segments:
                db.session.add(s)
            db.session.commit()
            return Response(json.dumps(event.dict_segments), mimetype="application/json")

    @expose('/edit/files', methods=('GET', ))
    def rest_files(self):
        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect( get_redirect_target() or self.get_url('.index_view'))

        event = self.get_one(id)

        if event is None:
            flash(gettext('Event does not exist.'), 'error')
            return redirect(return_url)

        files = []

        for f in VideoFile.query.filter(VideoFile.conference_id==event.conference.id,
                                        VideoFile.active==True, VideoFile.deleted==False):
            files.append(f.todict)

        return Response(json.dumps(files), mimetype="application/json")


