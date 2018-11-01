from flask import url_for, redirect, request, abort

from flask_admin.contrib import sqla
from flask_admin.form import SecureForm

from flask_security import current_user

class LoginView(sqla.ModelView):
    form_base_class = SecureForm
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        return True

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


class AdminView(LoginView):
    form_base_class = SecureForm

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True
        return super(AdminView, self).is_accessible()

class SystemView(LoginView):
    form_base_class = SecureForm

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('system'):
            return True
        return super(SystemView, self).is_accessible()

from .admin import AdminSegmentView, AdminFileView
from .video import EventCutView
