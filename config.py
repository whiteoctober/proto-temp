error_conditions = {
"age": {
        "not_present": "Please specify an age",
        "not_numeric": "Please give an age in years",
        "too_high": "The maximum value allowed is 99",
        "too_low": "The minimum value allowed is 16"
    },
"gender": {
        "not_present": "Please specify your gender",
    }
}

fields = {
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
            "title": "Basic questions",
            "fields": ["age", "gender"]
        }],
    }
}
