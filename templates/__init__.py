import cherrypy
from jinja2 import FileSystemLoader
from PressUI.utils.template_utils import press_get_env
env = press_get_env(FileSystemLoader("templates"))

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
