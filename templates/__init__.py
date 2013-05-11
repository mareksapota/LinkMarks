import cherrypy
from jinja2 import Environment, FileSystemLoader
env = Environment(loader = FileSystemLoader("templates"))
env.autoescape = True

import config

def render(tmpl, **kwargs):
    return render_template(tmpl + ".html", **kwargs)

def render_template(tmpl, **kwargs):
    t = env.get_template(tmpl)
    return t.render(
        fb_app_id = config.fb_app_id,
        hostname = cherrypy.request.base,
        **kwargs
    ).encode("utf-8")
