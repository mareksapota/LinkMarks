from jinja2 import Environment, FileSystemLoader
env = Environment(loader = FileSystemLoader("templates"))
env.autoescape = True

def render(tmpl, **kwargs):
    t = env.get_template(tmpl + ".html")
    return t.render(**kwargs)
