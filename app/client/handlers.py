import os

import lib.cloudstorage as gcs
import webapp2
from google.appengine.api import app_identity
from google.appengine.api import users

import config
import core.forms as forms
import form_config
from models import *
from core.handlers import *

class HomeHandler(BaseHandler):
    def get(self):
        self.render('index', {'welcome_message': 'Hello, world!'})

class FormHandler(BaseHandler):
    def get(self):
        # render the form using the form fields dictionary built using the forms.build_form_fields(form, variables) function
        # variables are an empty dictionary as the form isn't filled in yet
        self.render("sample_form", {
            "form": forms.build_form_fields("example", {}),
            "error_conditions": form_config.error_conditions
        })

    @check_origin_or_referer
    def post(self):
        form_name = "example"
        variable_set, errors = forms.build_variable_set(self, form_name)
        if len(errors) > 0:
            # render the form using the form fields dictionary built using the forms.build_form_fields(form, variables) function
            # variables are the variable_set dictionary from above
            self.render("sample_form", {
                "form": forms.build_form_fields(form_name, variable_set),
                "errors": errors,
                "error_conditions": form_config.error_conditions
            })
        else:
            # no errors, persist model and show the thanks page
            variable_set['age'] = int(variable_set['age'])
            person_object = Person(**variable_set) # unpack the dictionary object with ** to pass the contents to named parameters
            person_key = person_object.put()
            self.session.add_flash("Person created", "success")
            self.render('thanks', {'variable_set': variable_set, 'key': person_key, 'env': config.get_environment_name()})

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
