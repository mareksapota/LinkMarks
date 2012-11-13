#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cherrypy
from cherrypy.process.plugins import PIDFile
import os
import sys

import model
import templates as t

def safe_access(fn):

    @cherrypy.expose
    def wrapped(*args, **kwargs):
        try:
            if "token" in kwargs:
                token = kwargs.pop("token")
            else:
                token = cherrypy.request.cookie["token"].value
            model.Token.use(token)
        except:
            return t.render("expired")

        cherrypy.response.cookie["token"] = model.Token.issue()
        cherrypy.response.cookie["token"]["path"] = "/"

        return fn(*args, **kwargs)

    return wrapped

class SaveMe():
    @safe_access
    def index(self):
        return t.render("index")

    @safe_access
    def search(self, query = None, redirect = None):
        if query is None:
            raise cherrypy.HTTPRedirect("/")
        if query:
            key_bookmark = model.Bookmark.find_keyword(query.split()[0])
            if key_bookmark is not None:
                raise cherrypy.HTTPRedirect(key_bookmark.search(query))
        bookmarks = model.Bookmark.find_all(query)
        if redirect == "yes" and len(bookmarks) == 1:
            raise cherrypy.HTTPRedirect(bookmarks[0].url)
        return t.render('search', bookmarks = bookmarks, query = query)

    @safe_access
    def new(self):
        return t.render('new')

    @safe_access
    def save(self, name, url, keyword, id = None, back = None):
        if id is None:
            model.Bookmark.new(name, url, keyword)
        else:
            model.Bookmark.update(id, name, url, keyword)
        if back is None:
            raise cherrypy.HTTPRedirect("/")
        else:
            raise cherrypy.HTTPRedirect("/search?query=" + back)

    @safe_access
    def edit(self, id, back):
        bookmark = model.Bookmark.get(id)
        return t.render('edit', bookmark = bookmark, back = back)

    @safe_access
    def delete(self, id):
        model.Bookmark.delete(id)
        raise cherrypy.HTTPRedirect("/")

cherrypy.config.update({
    "server.socket_port": 8080,
})

if len(sys.argv) > 1 and sys.argv[1] == "production":
    cherrypy.config.update({
        "environment": "production"
    })
    PIDFile(cherrypy.engine, "/tmp/linkmarks.pid").subscribe()

conf = {}
for d in ["style", "script"]:
    p = os.path.abspath(d)
    for f in os.listdir(d):
        conf["/{0}/{1}".format(d, f)] = {
            "tools.staticfile.on": True,
            "tools.staticfile.filename": "{0}/{1}".format(p, f),
            "tools.staticfile.content_types": {
                "css": "text/css",
                "js": "application/javascript"
            }
        }

cherrypy.quickstart(SaveMe(), config = conf)
