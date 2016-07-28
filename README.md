# WO Starter App Engine code for prototypes

Scaffolding for a prototype project in AppEngine and Python

## Setup

Install the App Engine SDK for Python: https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python

To set up the libraries for Google Cloud Storage, run

    pip install GoogleAppEngineCloudStorageClient -t app/lib
    touch app/lib/__init__.py

Run `dev_appserver.py --storage_path ./.datastore ./app` from the project root.

(If you don't supply `--storage_path`, the default will be used, which is usually in `/tmp`.  This is basically fine, but you may find that it's cleared when you restart your machine, hence the recommendation to use a storage path in the project folder itself.)

Browse to the site on [http://localhost:8080/](http://localhost:8080/) and you'll see a list of pages and what features they demonstrate.

## Deployment

The `wo-starter-prototype` project does not exist on Google Cloud Platform.  However, you can still deploy this starter project to a new real project's account as part of testing.  For this, specify the application on the command line, which will override the setting in `app.yaml`.  For example:

    appcfg.py -A staging-real-app-com update ./app

For more details, run `appcfg.py --help` or see [https://cloud.google.com/appengine/docs/python/getting-started/deploying-the-application](https://cloud.google.com/appengine/docs/python/getting-started/deploying-the-application).

## Using it

If you build your project on this code, we recommend that you...

* Rename the `app/client` folder to something project-specific, e.g. `app/project-name-here`.
* Create a unique secret key and update the one in `main.py`.
