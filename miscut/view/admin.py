
from ..view import AdminView

class AdminSegmentView(AdminView):
    form_columns = ('event', 'videofile', 'segment_id', 'version', 'start', 'length', 'transition', 'transition_length', 'assigned')
    column_list =  ('event', 'videofile', 'segment_id', 'version', 'start', 'length', 'assigned', 'created_at', 'changed_at')
