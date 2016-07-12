import os
import socket

ROLE_ADMINISTRATOR = "administrator"

roles = {
    "admin@example.com": [
        ROLE_ADMINISTRATOR
    ],
    "sam@whiteoctober.co.uk": [
        ROLE_ADMINISTRATOR
    ],
}

ENVIRONMENT_DEV = "dev"
ENVIRONMENT_STAGING = "staging"
ENVIRONMENT_PRODUCTION = "production"

environments = {
    ENVIRONMENT_DEV: {
        "static_root": "/static",
        "bucket_name": "app_default_bucket",
    },
    ENVIRONMENT_STAGING: {
        "static_root": "/static",
        "bucket_name": "staging-yoursite-com.appspot.com",
    },
    ENVIRONMENT_PRODUCTION: {
        "static_root": "/static",
        "bucket_name": "www-yoursite-com.appspot.com",
    },
}

def get_environment_name():
    platform = os.getenv('SERVER_SOFTWARE') # e.g. Development/2.0 or Google App Engine/1.9.38
    if ("Development" in platform):
        return ENVIRONMENT_DEV

    host_name = socket.gethostname() # e.g. localhost:8080 or something.appspot.com
    # TODO You may want to update this specifically for your environment
    if ("staging" in host_name):
        return ENVIRONMENT_STAGING
    else:
        return ENVIRONMENT_PRODUCTION

def get_environment_setting(name):
    return environments[get_environment_name()][name]
