#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cherrypy
from cherrypy.process.plugins import PIDFile
import os
import os.path
import sys
import json

from utils.Query import query_arg, valid_query_arg
from utils.redirect import perform_redirect
from model.Bookmark import Bookmark
import model.Parse
import templates as t
import config

import python_apis_maarons.FB.login as FBlogin

model.Parse.init(config.parse_app_id, config.parse_rest_key)

def safe_access(fn):

    @cherrypy.expose
    def wrapped(*args, **kwargs):
        try:
            FBlogin.cherrypy_authenticate(
                config.fb_app_id,
                config.fb_app_secret,
            )
        except FBlogin.LoginException:
            return t.render("login")
        except:
            return t.render("accessdenied")

        if cherrypy.request.fb_user_id not in config.fb_allowed_user_ids:
            return t.render("accessdenied")

        return fn(*args, **kwargs)

    return wrapped

class LinkMarks():
    @safe_access
    def index(self, query = ""):
        return t.render("index", query = query)

    @safe_access
    @valid_query_arg("/")
    def search(self, query = None, redirect = None):
        key_bookmark_p = Bookmark.gen_find_keyword(query.keyword())
        bookmarks_p = Bookmark.gen_find_all(query)

        key_bookmark = key_bookmark_p.prep()
        if key_bookmark is not None:
            return perform_redirect(key_bookmark.search(query.body()))

        bookmarks = bookmarks_p.prep()
        if redirect == "yes" and len(bookmarks) == 1:
            return perform_redirect(bookmarks[0].str_url())
        return t.render(
            "search",
            bookmarks = bookmarks,
            query = query,
        )

    @safe_access
    def all(self):
        bookmarks = Bookmark.all()
        return t.render(
            "all",
            bookmarks = bookmarks,
        )

    @safe_access
    def new(self):
        return t.render("new")

    @safe_access
    def save(self, name, url, keyword, tags, suggestions_url, objectId = None, back = None):
        bookmark = Bookmark()
        if objectId is not None:
            bookmark = Bookmark.get_safe(objectId)
        bookmark.name = name if name.strip() else None
        bookmark.url = url if url.strip() else None
        bookmark.keyword = keyword if keyword.strip() else None
        bookmark.suggestions_url = suggestions_url if suggestions_url.strip() else None
        bookmark.tags = tags.strip()
        bookmark.save()
        if back is None:
            return perform_redirect("/")
        else:
            return perform_redirect(back)

    @safe_access
    def edit(self, objectId, back):
        bookmark = Bookmark.get_safe(objectId)
        return t.render("edit", bookmark = bookmark, back = back)

    @safe_access
    def delete(self, objectId, back = None):
        bookmark = Bookmark.get_safe(objectId)
        bookmark.destroy()
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
            limit = int(count)
            if query is None or not query.is_valid():
                raise Exception("Invalid query")
            user_agent = cherrypy.request.headers["User-Agent"]
            key_bookmark_p = Bookmark.gen_find_keyword(query.keyword())
            bookmarks_p = Bookmark.gen_find_all(query, limit = limit)
            key_bookmark = key_bookmark_p.prep()
            if key_bookmark is not None:
                results = key_bookmark.get_suggestions(query, user_agent, limit)
                if results is not None:
                    return json.dumps(results)
            return json.dumps([
                str(query.url_unsafe()),
                [b.name for b in bookmarks_p.prep()],
            ])
        except:
            return json.dumps([str(query.url_unsafe()), []])

    @safe_access
    def addengine(self):
        return t.render("addengine")

    @safe_access
    def version(self):
        f = os.path.abspath(__file__)
        d = os.path.dirname(f)
        linkmarks_version = "unknown"
        with open(d + "/.git/refs/heads/master") as f:
            linkmarks_version = f.read()
        pressui_version = "unknown"
        with open(d + "/PressUI/.git/refs/heads/master") as f:
            pressui_version = f.read()
        return t.render(
            "version",
            linkmarks_version = linkmarks_version,
            pressui_version = pressui_version,
        )

    @cherrypy.expose
    def channel(self):
        cherrypy.request.fb_user_id = None
        return t.render("PressUI/facebook_channel")

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
for (d, _, names) in os.walk("static", followlinks = True):
    p = os.path.abspath(d)
    for f in names:
        conf["/{0}/{1}".format(d, f)] = {
            "tools.staticfile.on": True,
            "tools.staticfile.filename": "{0}/{1}".format(p, f),
            "tools.staticfile.content_types": {
                "css": "text/css",
                "js": "application/javascript"
            }
        }

cherrypy.quickstart(LinkMarks(), config = conf)
