import webapp2
import templates
import forms
import config

from google.appengine.api import users

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, variables={}):
        templates.output_page(self, templates.render_page(self, template, variables))

class MainHandler(BaseHandler):
    def get(self, args):
        self.render('index', {'message': 'Hello, world!'})

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
            # no errors, show the thanks page
            self.render('thanks', {'variable_set': variable_set})

class RestrictedAreaHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            self.render('restricted', {'nickname': nickname, 'logout_url': logout_url})
        else:
            login_url = users.create_login_url('/restricted')
            return self.redirect(login_url)
