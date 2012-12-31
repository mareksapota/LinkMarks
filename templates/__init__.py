import cherrypy
from jinja2 import Environment, FileSystemLoader
env = Environment(loader = FileSystemLoader("templates"))
env.autoescape = True

def render(tmpl, **kwargs):
    return render_template(tmpl + ".html", **kwargs)

def render_template(tmpl, **kwargs):
    token = cherrypy.request.token
    t = env.get_template(tmpl)
    return t.render(token = token, **kwargs).encode("utf-8")
