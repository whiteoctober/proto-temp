#!/usr/bin/env python

import webapp2
from client import routes

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'todo-generate-a-unique-key-for-your-project',
}

### Main app, routed from app.yaml
app = webapp2.WSGIApplication(routes.ROUTES, debug=True, config=config)
