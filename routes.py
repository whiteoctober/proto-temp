import handlers as handlers

ROUTES = [
    ('/sample-form', handlers.FormHandler),
    ('/(.*)', handlers.MainHandler),
]
