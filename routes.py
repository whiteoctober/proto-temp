import handlers as handlers

ROUTES = [
    ('/sample-form', handlers.FormHandler),
    ('/restricted-inline', handlers.RestrictedAreaHandler),
    ('/restricted', handlers.RestrictedByDecoratorHandler),
    ('/(.*)', handlers.MainHandler),
]
