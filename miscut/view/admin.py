
from ..view import AdminView

class AdminSegmentView(AdminView):
    form_columns = ('event', 'videofile', 'segment_id', 'version', 'start', 'length', 'transition', 'transition_length', 'assigned')
    column_list =  ('event', 'videofile', 'segment_id', 'version', 'start', 'length', 'assigned', 'created_at', 'changed_at')


class AdminFileView(AdminView):
    can_view_details = True
    column_searchable_list = ('conference.name', 'storage_url', 'file_url')
    details_template = 'file_details.html'
