import cherrypy

def perform_redirect(url):
    raise cherrypy.HTTPRedirect(url)
