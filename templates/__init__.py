from jinja2 import Environment, FileSystemLoader
env = Environment(loader = FileSystemLoader("templates"))
env.autoescape = True

def render(tmpl, **kwargs):
    return render_template(tmpl + ".html", **kwargs)

def render_template(tmpl, **kwargs):
    t = env.get_template(tmpl)
    return t.render(**kwargs).encode("utf-8")
