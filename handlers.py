import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self, args):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')
