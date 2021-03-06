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
        "max": 99,
        "help_text": "Min 16; max 99.",
    },
    "gender": {
        "label": "Gender",
        "type": "radio",
        "options": ["male", "female"]
    },
    "example-select": {
        "label": "Example Select box",
        "type": "select",
        "options": {"value-stored": "What's displayed", "value-stored2": "What's displayed2"}
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
