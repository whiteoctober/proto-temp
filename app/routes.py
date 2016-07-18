import handlers
import webapp2
from webapp2_extras import routes as extras_routes

ROUTES = [
    # use a broad regular expression for site url as this is a sample project
    # TODO update this to something better in your real project
    extras_routes.DomainRoute(r'<:static\..*\.\w+>', [
        webapp2.Route('/<fileurl>', handler=handlers.GCSHandler, name='static-gcs'),
    ]),
    webapp2.Route('/sample-form', handler=handlers.FormHandler, name="form"),
    webapp2.Route('/restricted-inline', handler=handlers.RestrictedAreaHandler, name="restricted-inline"),
    webapp2.Route('/restricted', handler=handlers.RestrictedByDecoratorHandler, name="restricted"),
    webapp2.Route('/restricted-app-engine', handler=handlers.RestrictedByAppEngineDecoratorHandler, name="restricted-app-engine"),
    webapp2.Route('/restricted-role', handler=handlers.RestrictedByRoleDecoratorHandler, name="restricted-role"),
    webapp2.Route('/', handler=handlers.HomeHandler, name="home"),
]
