import webapp2
import templates as templates

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, variables):
        templates.output_page(self, templates.render_page(self, template, variables))

class MainHandler(BaseHandler):
    def get(self, args):
        self.render('index', {'message': 'Hello, world!'})
