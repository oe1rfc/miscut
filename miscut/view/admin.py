
from ..view import AdminView

class AdminSegmentView(AdminView):
    form_columns = ('event', 'videofile', 'segment_id', 'version', 'start', 'length', 'transition', 'transition_length', 'assigned')
    column_list =  ('event', 'videofile', 'segment_id', 'version', 'start', 'length', 'assigned', 'created_at', 'changed_at')

class AdminFileView(AdminView):
    can_view_details = True
    column_searchable_list = ('conference.name', 'storage_url', 'file_url')
    details_template = 'file_details.html'
    column_editable_list = ('active', 'deleted', 'comment')

class AdminEventView(AdminView):
    can_view_details = True
    column_searchable_list = ('conference.name', 'event_id', 'name', 'subtitle', 'personnames')
    column_exclude_list = ('subtitle', 'duration', 'rendered_url', 'created_at', 'description_updated', 'changed_at')
    column_editable_list = ('active', 'state', 'comment')
