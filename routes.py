import handlers as handlers

ROUTES = [
    ('/sample-form', handlers.FormHandler),
    ('/restricted', handlers.RestrictedAreaHandler),
    ('/(.*)', handlers.MainHandler),
]
