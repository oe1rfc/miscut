from flask_admin.actions import action
from flask import flash

from ..view import AdminView
from ..model import db

class AdminSegmentView(AdminView):
    form_columns = ('event', 'videofile', 'segment_id', 'version', 'start', 'length', 'transition', 'transition_length', 'assigned')
    column_list =  ('event', 'videofile', 'segment_id', 'version', 'start', 'length', 'assigned', 'created_at', 'changed_at')
    column_searchable_list = ('event.event_id', 'event.conference.code', 'videofile.storage_url')
    column_filters = ('event.event_id', 'event.conference.code', 'videofile.storage_url', 'videofile.type', 'segment_id', 'version', 'assigned', 'created_at', 'changed_at')

class AdminFileView(AdminView):
    can_view_details = True
    column_searchable_list = ('conference.name', 'conference.code', 'storage_url', 'file_url')
    details_template = 'file_details.html'
    column_editable_list = ('active', 'deleted', 'comment')
    column_filters = ('conference.code', 'type','active', 'deleted')

    @action('deactivate', 'Deactivate', 'Are you sure you want to deactivate entries?')
    def action_deactivate(self, ids):
        try:
            query = self.model.query.filter(self.model.id.in_(ids))
            count = 0
            for e in query.all():
                e.active = False
                count += 1
            db.session.commit()
            flash('%s successfully deactivated.' % count)
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(gettext('Failed: %(error)s', error=str(ex)), 'error')

    @action('activate', 'Activate', 'Are you sure you want to activate entries?')
    def action_activate(self, ids):
        try:
            query = self.model.query.filter(self.model.id.in_(ids))
            count = 0
            for e in query.all():
                e.active = True
                count += 1
            db.session.commit()
            flash('%s successfully activated.' % count)
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(gettext('Failed: %(error)s', error=str(ex)), 'error')


class AdminEventView(AdminView):
    can_view_details = True
    column_searchable_list = ('conference.name', 'event_id', 'name', 'subtitle', 'personnames')
    column_exclude_list = ('subtitle', 'duration', 'rendered_url', 'created_at', 'description_updated', 'changed_at')
    column_editable_list = ('active', 'state', 'comment', 'record')
    column_filters = ('conference.code', 'active', 'state', 'record', 'room')

    @action('deactivate', 'Deactivate', 'Are you sure you want to deactivate entries?')
    def action_deactivate(self, ids):
        try:
            query = self.model.query.filter(self.model.id.in_(ids))
            count = 0
            for e in query.all():
                e.active = False
                count += 1
            db.session.commit()
            flash('%s successfully deactivated.' % count)
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(gettext('Failed: %(error)s', error=str(ex)), 'error')

    @action('activate', 'Activate', 'Are you sure you want to activate entries?')
    def action_activate(self, ids):
        try:
            query = self.model.query.filter(self.model.id.in_(ids))
            count = 0
            for e in query.all():
                e.active = True
                count += 1
            db.session.commit()
            flash('%s successfully activated.' % count)
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(gettext('Failed: %(error)s', error=str(ex)), 'error')
