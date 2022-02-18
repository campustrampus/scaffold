""" api admin

Admin routes for the admin portal
"""
from flask_admin import AdminIndexView, expose
from flask import current_app, url_for
from app.auth import require_scope
from app.errors import AuthError, get_scope_insufficient_error_message


class AuthAdminIndexView(AdminIndexView):
    """ Admin Index View
    """
    @expose('/')
    def index(self):
        """ index route for admin view
        :return: str
        """
        return super().index()

    # pylint: disable=no-self-use
    @expose('/logout')
    def logout(self):
        """ logout route for admin view
        :return: str
        """
        return 'Logged out?'

    def get_url(self, endpoint, **kwargs):
        """
        Generate URL for the endpoint. If you want to customize URL generation
        logic (persist some query string argument, for example), this is
        right place to do it.
        :param endpoint:
            Flask endpoint name
        :param kwargs:
            Arguments for `url_for`
        """
        admin_url_scheme = current_app.config['ADMIN_URL_SCHEME']

        return url_for(endpoint,
                       **kwargs,
                       _scheme=admin_url_scheme,
                       _external=True)
