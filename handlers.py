import webapp2
import templates
import forms
import config
import os
import lib.cloudstorage as gcs
from models import *
from google.appengine.api import app_identity

from google.appengine.api import users

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
        templates.output_page(self, templates.render_page(self, template, variables))

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

class HomeHandler(BaseHandler):
    def get(self):
        self.render('index', {'welcome_message': 'Hello, world!'})

class FormHandler(BaseHandler):
    def get(self):
        # render the form using the form fields dictionary built using the forms.build_form_fields(form, variables) function
        # variables are an empty dictionary as the form isn't filled in yet
        self.render("form", {
            "form": forms.build_form_fields("example", {})
        })

    def post(self):
        form_name = "example"
        # create an array to collect form field errors in
        # if the length of the array is zero, output the form again
        variable_set, errors = forms.build_variable_set(self, form_name)
        if len(errors) > 0:
            # render the form using the form fields dictionary built using the forms.build_form_fields(form, variables) function
            # variables are the variable_set dictionary from above
            self.render("form", {
                "form": forms.build_form_fields(form_name, variable_set),
                "errors": errors,
                "error_conditions": config.error_conditions
            })
        else:
            # no errors, persist model and show the thanks page
            variable_set['age'] = int(variable_set['age'])
            person_object = Person(**variable_set) # unpack the dictionary object with ** to pass the contents to named parameters
            person_key = person_object.put()
            self.render('thanks', {'variable_set': variable_set, 'key': person_key})

class RestrictedAreaHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            self.render('restricted', {'nickname': nickname, 'logout_url': logout_url, 'extra_message': ''})
        else:
            login_url = users.create_login_url('/restricted-inline')
            return self.redirect(login_url)

class RestrictedByDecoratorHandler(BaseHandler):
    @login_required
    def get(self):
        user = users.get_current_user() # we know this is defined, thanks to the decorator
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        self.render('restricted', {'nickname': nickname, 'logout_url': logout_url})

class RestrictedByAppEngineDecoratorHandler(BaseHandler):
    @app_engine_login_required
    def get(self):
        user = users.get_current_user() # we know this is defined, thanks to the decorator
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        self.render('restricted', {'nickname': nickname, 'logout_url': logout_url, 'extra_message': 'Only users with App Engine permissions here!'})

class RestrictedByRoleDecoratorHandler(BaseHandler):
    @role_required(config.ROLE_ADMINISTRATOR)
    def get(self):
        user = users.get_current_user() # we know this is defined, thanks to the decorator
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        self.render('restricted', {'nickname': nickname, 'logout_url': logout_url, 'extra_message': 'You\'ve got the role we wanted!'})

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
