# WO Starter App Engine code for prototypes

Scaffolding for a prototype project in AppEngine and Python

## Setup

Install the App Engine SDK for Python: https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python

Run `dev_appserver.py .` from the project root.

Browse to the site on [http://localhost:8080/](http://localhost:8080/)

## What you get

You can see a very simple sample route which uses the helper functions for Jinja templating at [http://localhost:8080/](http://localhost:8080/)

You can see a route which uses the form library at [http://localhost:8080/sample-form](http://localhost:8080/sample-form)

[http://localhost:8080/restricted-inline](http://localhost:8080/restricted-inline) is an example of a page restricted by the [Python Users API](https://cloud.google.com/appengine/docs/python/users/).

[http://localhost:8080/restricted](http://localhost:8080/restricted) is the same thing but accomplished using a [decorator](http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/).  Just add `@login_required` above your `get` and `set` methods to make them require authentication!
