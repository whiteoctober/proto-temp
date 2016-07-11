import handlers as handlers

ROUTES = [
    webapp2.Route('/sample-form', handler=handlers.FormHandler, name="form"),
    webapp2.Route('/restricted-inline', handler=handlers.RestrictedAreaHandler, name="restricted-inline"),
    webapp2.Route('/restricted', handler=handlers.RestrictedByDecoratorHandler, name="restricted"),
    webapp2.Route('/restricted-app-engine', handler=handlers.RestrictedByAppEngineDecoratorHandler, name="restricted-app-engine"),
    webapp2.Route('/restricted-role', handler=handlers.RestrictedByRoleDecoratorHandler, name="restricted-role"),
    webapp2.Route('/', handler=handlers.HomeHandler, name="home"),
]
