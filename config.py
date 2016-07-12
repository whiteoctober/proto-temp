import os
import socket

error_conditions = {
    "name": {
        "not_present": "Please tell us your name",
    },
    "age": {
        "not_present": "Please specify an age",
        "not_numeric": "Please give an age in years",
        "too_high": "The maximum value allowed is 99",
        "too_low": "The minimum value allowed is 16"
    },
}

fields = {
    "name": {
        "label": "Name",
        "type": "text"
    },
    "age": {
        "label": "Age (in years)",
        "type": "number",
        "min": 16,
        "max": 99
    },
    "gender": {
        "label": "Gender",
        "type": "radio",
        "options": ["male", "female"]
    },
}

forms = {
    "example": {
        "sections":[{
            "key": "first",
            "title": "Create a Person model",
            "fields": ["name", "age", "gender"]
        }],
    }
}

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
    },
    ENVIRONMENT_STAGING: {
        "static_root": "/static",
    },
    ENVIRONMENT_PRODUCTION: {
        "static_root": "/static",
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
