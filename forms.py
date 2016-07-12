import form_config

# takes the description of the form and then appends the description of the field and the value if appropriate
def build_form_fields(form, variables):
    # counter so each of the fields can be numbered
    i = 0
    # pull in the definition of the sections of the form from the config file
    sections = form_config.forms[form]["sections"]
    # iterate through the sections
    for section in sections:
        # create a blank fieldset for the section
        section["fieldset"] = []
        # iterate through the fields
        for field in section["fields"]:
            # increment the counter
            i+=1
            # load the relevant field description from the config file
            fielddescription = form_config.fields[field]
            # add a key which is set to the field name
            fielddescription["key"] = field
            # add a order number for the field
            fielddescription["number"] = i
            # if there's a value for the field, then add it here, if not set it to False
            if variables.has_key(field):
                fielddescription["value"] = variables[field]
            else:
                fielddescription["value"] = False
            # then append the field description to the fieldset in the section
            section["fieldset"].append(fielddescription)
    # return the sections
    return sections


# retrieves the variable from the request
def retrieve_variable(self, field_name):
    # initialise an errors array
    errors = []
    # set the variable to False as the default
    variable = False
    # if the field is one we need to check for errors
    if form_config.error_conditions.has_key(field_name):
        # try to get the variable from the request
        if self.request.get(field_name):
            # set the variable to the relevant variable from the request
            variable = self.request.get(field_name)
            # if there is an error condition for it being an int or not then test it here
            if form_config.error_conditions[field_name].has_key("not_numeric"):
                try:
                    # cast the variable to a variable
                    variable = float(variable)

                    if form_config.fields[field_name].has_key("max") and variable > form_config.fields[field_name]["max"]:
                        errors.append("too_high")
                    if form_config.fields[field_name].has_key("min") and variable < form_config.fields[field_name]["min"]:
                        errors.append("too_low")
                except:
                    # add the key for the error to the errors array
                    errors.append("not_numeric")
        else:
            # if there's an error condition for the variable being empty
            if form_config.error_conditions[field_name].has_key("not_present"):
                # add the key for the error to the errors array
                errors.append("not_present")
    else:
        # if there's no error conditions for the field, optimisticly attempt to set the variable to the one from the request
        variable = self.request.get(field_name)
    return variable, errors


# builds a set of all the variables
def build_variable_set(self, form):
    # an empty array of the fields in the form
    field_set = []
    # an empty dictionary of the fields errors
    error_set = {}
    # an empty set of all the variables which will be used for the calculation of the score
    variable_set = {}
    # iterate through the sections in the form
    for section in form_config.forms[form]["sections"]:
        # append the array of the fields in the section to the array of all fields
        field_set += section["fields"]
    # iterate through the array of fields
    for field in field_set:
        # retrieve the value and any errors for that field
        value, errors = retrieve_variable(self, field)
        # add a key/value pair in the variable_set dictionary for the field and the value
        variable_set[field] = value
        # if there are errors then add them to a dictionary of errors
        if errors:
            error_set[field] = errors
    # return the error and variable dictionaries
    return variable_set, error_set
