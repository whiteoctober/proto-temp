import handlers as handlers

ROUTES = [
    ('/sample-form', handlers.FormHandler),
    ('/restricted-inline', handlers.RestrictedAreaHandler),
    ('/restricted', handlers.RestrictedByDecoratorHandler),
    ('/restricted-app-engine', handlers.RestrictedByAppEngineDecoratorHandler),
    ('/', handlers.HomeHandler),
]
