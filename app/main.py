#!/usr/bin/env python

import webapp2
import client.routes as routes

### Main app, routed from app.yaml
app = webapp2.WSGIApplication(routes.ROUTES, debug=True)
