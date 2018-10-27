
from ..view import AdminView

class AdminSegmentView(AdminView):
    form_columns = ('event', 'videofile', 'segment_id', 'version', 'start', 'length', 'transition', 'assigned')
    column_list =  ('event', 'videofile', 'segment_id', 'version', 'start', 'length', 'assigned', 'created_at', 'changed_at')
