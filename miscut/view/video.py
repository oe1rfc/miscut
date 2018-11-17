
from flask_admin.base import expose

from flask import request, redirect, flash, abort, json, Response
from flask_admin.helpers import get_redirect_target
from flask_admin.babel import gettext

from sqlalchemy.sql.expression import func
from flask_admin.model.helpers import get_mdict_item_or_list

from wtforms import Form, StringField
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.model.fields import AjaxSelectField, AjaxSelectMultipleField

from ..view import LoginView
from ..model import db, VideoFile, VideoSegment, Event


class EventCutView(LoginView):
    can_delete = False
    can_create = False
    can_view_details = False
    column_exclude_list = ('subtitle', 'duration', 'rendered_url', 'created_at', 'description_updated', 'changed_at')
    column_searchable_list = ('conference.name', 'event_id', 'name', 'subtitle', 'personnames', 'comment')

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
            if 'segments' not in saved or 'render' not in saved:
                abort(400)
            newversion = (event.version + 1)
            segments = []
            for s in saved['segments']:
                videofile=VideoFile.query.filter_by(id=int(s['videofile_id'])).first()
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
            event.version = newversion
            if saved['render'] is True:
                event.state = 'rendering'
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


class EventReleaseView(LoginView):
    can_delete = False
    can_create = False
    can_view_details = False
    edit_template = 'event_release.html'
    column_exclude_list = ('subtitle', 'duration', 'rendered_url', 'created_at', 'description_updated', 'changed_at')
    column_searchable_list = ('conference.name', 'event_id', 'name', 'subtitle', 'personnames', 'comment')

    def create_view(self):
        pass
    def delete_view(self):
        pass
    def ajax_update(self):
        pass

    def get_query(self):
        return super(EventReleaseView, self).get_query().filter(self.model.state == 'checking',
                                                                                                self.model.active == True,
                                                                                                self.model.rendered_url != None)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.state == 'checking',
                                                                                    self.model.active == True,
                                                                                    self.model.rendered_url != None)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        if request.method == 'GET':
            return super(EventReleaseView, self).edit_view()
        else:
            super(EventReleaseView, self).edit_view()
            return redirect(self.get_url('.index_view'))

    class FileReleaseForm(Form):
        comment = StringField('File Comment')

    def edit_form(self, obj=None):
        return self.FileReleaseForm(data={'comment': obj.comment})

    def update_model(self, form, model):
        print(request.form)
        if 'comment' in request.form:
            model.comment = request.form['comment']
        if '_set_recut' in request.form:
            model.state = 'cutting'
        elif model.record is True:
            model.state = 'published'
        db.session.commit()



class FileAssignView(LoginView):
    can_delete = False
    can_create = False
    can_view_details = False
    edit_template = 'file_assign.html'

    column_exclude_list = ('startdate', 'storage_url', 'created_at', 'changed_at', 'deleted', 'active')
    column_searchable_list = ('conference.name', 'conference.code', 'file_url', 'comment')

    def create_view(self):
        pass
    def delete_view(self):
        pass
    def ajax_update(self):
        pass

    def get_query(self):
        return super(FileAssignView, self).get_query().outerjoin(VideoSegment).filter(self.model.deleted == False,
                                                                                      self.model.active == True,
                                                                                      VideoSegment.event_id == None)

    def get_count_query(self):
        return self.session.query(func.count(self.model.id)).outerjoin(VideoSegment).filter(self.model.deleted == False,
                                                                                      self.model.active == True,
                                                                                      VideoSegment.event_id == None)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        if request.method == 'GET':
            return super(FileAssignView, self).edit_view()
        else:
            super(FileAssignView, self).edit_view()
            return redirect(self.get_url('.index_view'))

    def update_model(self, form, model):
        if 'comment' in request.form:
            model.comment = request.form['comment']
        if '_set_inactive' in request.form:
            model.active = False
        else:
            segments = []
            for eid in request.form['assign_events'].split(','):
                event = Event.query.filter_by(id=eid).first()
                if event and event.conference_id is model.conference_id and event.state in ('stub', 'cutting'):
                    segments.append(VideoSegment(
                        event = event,
                        version = event.version,
                        segment_id = len(list(event.segments)) + 1,
                        videofile = model,
                        start = 0,
                        length = model.length
                        )
                    )
            for s in segments:
                db.session.add(s)
        db.session.commit()


    class FileAssignForm(Form):
        assign_events = AjaxSelectMultipleField(loader=None)
        comment = StringField('File Comment')

    def get_event_loader(self, conference_id):
        return QueryAjaxModelLoader(
            conference_id,
            db.session, Event,
            fields=['name', 'personnames'],
            page_size=10,
            placeholder="Search for Events",
            filters = (Event.conference_id == conference_id)
        )

    def edit_form(self, obj=None):
        form = self.FileAssignForm(data={'comment': obj.comment})
        form.assign_events.loader = self.get_event_loader(obj.conference_id)
        return form

    @expose('/ajax/lookup/')
    def ajax_lookup(self):
        conference_id = request.args.get('name', type=int)
        query = request.args.get('query')
        offset = request.args.get('offset', type=int)
        limit = request.args.get('limit', 10, type=int)

        loader = self.get_event_loader(conference_id)
        if not loader:
            abort(404)

        data = [loader.format(m) for m in loader.get_list(query, offset, limit)]
        return Response(json.dumps(data), mimetype='application/json')


class EventOverView(LoginView):
    can_delete = False
    can_create = False
    can_edit = False
    can_view_details = False
    column_exclude_list = ('subtitle', 'duration', 'rendered_url', 'created_at', 'description_updated', 'changed_at')
    column_searchable_list = ('conference.name', 'event_id', 'name', 'subtitle', 'personnames', 'comment')
    column_filters = ('conference.code', 'state', 'room', 'record')
    column_default_sort = ('changed_at', True)

    def create_view(self):
        pass
    def delete_view(self):
        pass
    def edit_view(self):
        pass
    def ajax_update(self):
        pass

    def get_query(self):
        return super(EventOverView, self).get_query().filter(self.model.active == True)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.active == True)
