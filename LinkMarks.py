#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cherrypy
from cherrypy.process.plugins import PIDFile
import os
import sys
import json

from utils.Query import query_arg, valid_query_arg
from utils.redirect import perform_redirect
import model
import templates as t

# Stop if schema version doesn’t match supported version.
model.SchemaVersion.check_version()

def safe_access(fn):

    @cherrypy.expose
    def wrapped(*args, **kwargs):
        try:
            if "token" in kwargs:
                token = kwargs.pop("token")
            else:
                token = cherrypy.request.cookie["token"].value
            # Save the token so actions can use it.
            cherrypy.request.token = token
            model.Token.use(token)
        except:
            return t.render("expired", token = None)

        cherrypy.response.cookie["token"] = model.Token.issue()
        cherrypy.response.cookie["token"]["path"] = "/"

        return fn(*args, **kwargs)

    return wrapped

class LinkMarks():
    @safe_access
    def index(self):
        return t.render("index")

    @safe_access
    @valid_query_arg("/")
    def nosearch(self, query = None):
        return t.render("nosearch", query = query);

    @safe_access
    @valid_query_arg("/")
    def search(self, query = None, redirect = None):
        key_bookmark = model.KeywordBookmark.find(query.keyword())
        if key_bookmark is not None:
            return perform_redirect(key_bookmark.search(query.body()))

        bookmarks = model.BookmarkBase.find_all(query)
        if redirect == "yes" and len(bookmarks) == 1:
            return perform_redirect(bookmarks[0].get_url())
        return t.render(
            "search",
            bookmarks = bookmarks,
            query = query,
        )

    @safe_access
    def all(self):
        bookmarks = model.BookmarkBase.all()
        return t.render(
            "all",
            bookmarks = bookmarks,
        )

    @safe_access
    def new(self):
        return t.render("new")

    @safe_access
    def save(self,name, url, keyword, tags, suggestions_url, id = None, back = None):
        if id is None:
            model.BookmarkBase.new(name, url, keyword, tags, suggestions_url)
        else:
            bookmark = model.BookmarkBase.get(id)
            bookmark.update(name, url, keyword, tags, suggestions_url)
        if back is None:
            return perform_redirect("/")
        else:
            return perform_redirect(back)

    @safe_access
    def edit(self, id, back):
        bookmark = model.BookmarkBase.get(id)
        return t.render("edit", bookmark = bookmark, back = back)

    @safe_access
    def delete(self, id, back = None):
        model.Bookmark.delete(id)
        if back is None:
            return perform_redirect("/")
        else:
            return perform_redirect(back)

    # OpenSearch
    @safe_access
    def opensearchdescription_xml(self):
        cherrypy.response.headers['Content-Type'] = \
            "application/opensearchdescription+xml"
        host = cherrypy.request.base
        return t.render_template("opensearchdescription.xml", host = host)

    @safe_access
    @query_arg
    def suggestion(self, count, query = None):
        try:
            if query is None or not query.is_valid():
                raise Exception("Invalid query")
            user_agent = cherrypy.request.headers["User-Agent"]
            key_bookmark = model.KeywordBookmark.find(query.keyword())
            if key_bookmark is not None:
                results = key_bookmark.get_suggestions(query, user_agent)
                if results is not None:
                    return json.dumps(results)
            bookmarks = model.BookmarkBase.find_all(query, int(count))
            return json.dumps([
                str(query.url_unsafe()),
                [b.name for b in bookmarks],
            ])
        except:
            return json.dumps([str(query.url_unsafe()), []])

    @safe_access
    def addengine(self):
        host = cherrypy.request.base
        return t.render("addengine", host = host)

cherrypy.config.update({
    "server.socket_port": 8080,
    "tools.gzip.on": True,
})

if len(sys.argv) > 1 and sys.argv[1] == "production":
    cherrypy.config.update({
        "environment": "production",
        "tools.proxy.on": True
    })
    PIDFile(cherrypy.engine, "/tmp/linkmarks.pid").subscribe()

conf = {}
for d in ["static/style", "static/script"]:
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

cherrypy.quickstart(LinkMarks(), config = conf)
