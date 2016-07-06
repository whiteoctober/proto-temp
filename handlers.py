import webapp2
import templates as templates

class MainHandler(webapp2.RequestHandler):
    def get(self, args):
        templates.render(self, 'index', {'message': 'Hello, world!'})
