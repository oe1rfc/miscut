from flask_admin.contrib import sqla
from sqlalchemy.sql.expression import func

from ..view import LoginView
from ..model import db, VideoFile, VideoSegment, Event


class ReleasedEvents(sqla.ModelView):
    can_delete = False
    can_create = False
    can_edit = False
    can_view_details = True
    column_list = ('conference', 'name', 'personnames')
    column_searchable_list = ('conference.name', 'conference.code', 'event_id', 'name', 'subtitle', 'personnames')
    column_default_sort = ('changed_at', True)
    details_template = 'event_published.html'

    def create_view(self):
        pass
    def delete_view(self):
        pass
    def edit_view(self):
        pass
    def ajax_update(self):
        pass

    def get_query(self):
        return super(ReleasedEvents, self).get_query().filter(self.model.active == True, self.model.state == 'published', self.model.rendered_url != None)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.active == True, self.model.state == 'published', self.model.rendered_url != None)
