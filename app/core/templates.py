import jinja2
import os

### TEMPLATING FUNCTIONS ###

# set the Jinja environment using autoescaping of html and using the file system loader for templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(['client/templates', 'core/templates']),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# super simple template renderer

def render_page(self, template, variables):
    # builds the path to the template
    if not ".html" in template:
        template += ".html"
    # loads it into the Jinja environment
    template = JINJA_ENVIRONMENT.get_template(template)
    # outputs the HTML from the rendered template and variables
    return template.render(variables)

def output_page(self, html):
    # outputs the HTML from the rendered template and variables
    self.response.out.write(html)
