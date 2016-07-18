import os

import lib.cloudstorage as gcs
import webapp2
from google.appengine.api import app_identity
from google.appengine.api import users
from webapp2_extras import sessions

import client.config as config
import forms
import client.form_config as form_config
import templates
from client.models import *

def login_required(get_or_post_method):
    def inner_login_checker(self, *args, **kwargs):
        if users.get_current_user():
            return get_or_post_method(self, *args, **kwargs)
        else:
            login_url = users.create_login_url(self.request.path)
            return self.redirect(login_url)
    return inner_login_checker

def app_engine_login_required(get_or_post_method):
    def inner_login_checker(self, *args, **kwargs):
        if users.get_current_user() and users.is_current_user_admin():
            return get_or_post_method(self, *args, **kwargs)
        else:
            login_url = users.create_login_url(self.request.path)
            return self.redirect(login_url)
    return inner_login_checker

def role_required(role):
    def the_decorator(get_or_post_method):
        def inner_login_checker(self, *args, **kwargs):
            if users.get_current_user():
                # check they have the right role
                nickname = users.get_current_user().nickname()
                if (
                    nickname in config.roles and
                    role in config.roles[nickname]
                ):
                    return get_or_post_method(self, *args, **kwargs)
                else:
                    self.abort(403)
            else:
                login_url = users.create_login_url(self.request.path)
                return self.redirect(login_url)
        return inner_login_checker
    return the_decorator

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, variables={}):
        # add in additional "global" Jinja variables, available to every page
        variables["flash_messages"] = self.session.get_flashes()
        variables["static_root"] = config.get_environment_setting("static_root")
        templates.output_page(self, templates.render_page(self, template, variables))

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def handle_exception(self, exception, debug):
        if isinstance(exception, webapp2.HTTPException):
            if exception.code == 403:
                user = users.get_current_user()
                logout_url = None
                if user:
                    nickname = user.nickname
                    logout_url = users.create_logout_url('/')
                return self.render('errors/403', {'user': user, 'logout_url': logout_url})

        # Fall back to the usual error handling
        super(BaseHandler, self).handle_exception(exception, debug)

class GCSHandler(BaseHandler):
    def get_content_type(self, filename):
        stat = gcs.stat(filename)
        return stat.content_type

    def read_file(self, filename):
        gcs_file = gcs.open(filename)
        the_file = gcs_file.read()
        gcs_file.close()
        return the_file, self.get_content_type(filename)

    def get(self, fileurl):
        bucket_name = config.get_environment_setting("bucket_name")
        filename = "/" + bucket_name + "/" + fileurl
        try:
            the_file, content_type = self.read_file(filename)
        except gcs.errors.NotFoundError:
            self.abort(404)
        self.response.headers["Content-Type"] = content_type
        self.response.write(the_file)
