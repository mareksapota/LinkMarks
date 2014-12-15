#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cherrypy
import urllib.parse

from PressUI.cherrypy.PressApp import PressApp
from PressUI.cherrypy.PressConfig import PressConfig
from PressUI.cherrypy.server import quickstart
from PressUI.utils.browser_cache import add_cache_control_header
from model.Bookmark import Bookmark
import PressUI.API.FB.login as FBlogin
import model.Parse

def safe_access(fn):

    @cherrypy.expose
    def wrapped(*args, **kwargs):
        try:
            FBlogin.cherrypy_authenticate(
                PressConfig.get('fb_app_id'),
                PressConfig.get('fb_app_secret'),
            )
        except:
            raise Exception('Access denied')

        allowed_ids = PressConfig.get('fb_allowed_user_ids')
        if cherrypy.request.fb_user_id not in allowed_ids:
            raise Exception('Access denied')

        return fn(*args, **kwargs)

    return wrapped

class LinkMarks(PressApp):
    def _js_sources(self):
        return [
            'components/Bookmark.js',
            'components/BookmarkList.js',
            'components/BookmarkEdit.js',
            'controller/index.js',
            'controller/login.js',
            'controller/show_all.js',
            'controller/add_engine.js',
            'controller/search.js',
            'controller/new.js',
            'controller/edit.js',
            'controller/main.js',
        ]

    @cherrypy.tools.allow(methods = ['GET'])
    @cherrypy.expose
    def fb_login_info_json(self):
        ret = self._json({
            'app_id': PressConfig.get('fb_app_id'),
            'hostname': cherrypy.request.base,
        })
        add_cache_control_header(years = 1)
        return ret

    @cherrypy.tools.allow(methods = ["GET"])
    @safe_access
    def show_all_json(self):
        bookmarks = Bookmark.all()
        ret = self._json(list(map(lambda b: b.to_json(), bookmarks)))
        add_cache_control_header(days = 1)
        return ret

    def __search_common(self, query, key_transform):
        query = urllib.parse.unquote_plus(query)
        if len(query.strip()) == 0:
            return {'keyword': False, 'bookmarks': []}
        keyword = query.split()[0]

        key_bookmark_p = Bookmark.gen_find_keyword(keyword)
        bookmarks_p = Bookmark.gen_find_all(query)

        key_bookmark = key_bookmark_p.prep()
        if key_bookmark is not None:
            term = urllib.parse.quote_plus(query[len(keyword) + 1:])
            key_ret = key_transform(key_bookmark, keyword, term)
            if key_ret is not None:
                return {'keyword': True, 'ret': key_ret}

        bookmarks = bookmarks_p.prep()
        return {'keyword': False, 'bookmarks': bookmarks}

    @cherrypy.tools.allow(methods = ["GET"])
    @safe_access
    def search_json(self, query):
        def key_transform(key_bookmark, keyword, term):
            return key_bookmark.search(term)
        ret = self.__search_common(query, key_transform)
        if ret['keyword']:
            ret['url'] = ret['ret']
        else:
            ret['bookmarks'] = list(map(
                lambda b: b.to_json(),
                ret['bookmarks'],
            ))
        ret = self._json(ret)
        add_cache_control_header(days = 1)
        return ret

    @cherrypy.tools.allow(methods = ["GET"])
    @safe_access
    def suggestion(self, count, query):
        def key_transform(key_bookmark, keyword, term):
            nonlocal count
            user_agent = cherrypy.request.headers["User-Agent"]
            try:
                count = int(count)
                suggestions = key_bookmark.get_suggestions(
                    term,
                    user_agent,
                    count,
                )
                return ['{} {}'.format(keyword, s) for s in suggestions]
            except:
                return None
        ret = self.__search_common(query, key_transform)
        if ret['keyword']:
            results = ret['ret']
        else:
            results = [b.name for b in ret['bookmarks']]
        return self._json([query, results])

    @cherrypy.tools.allow(methods = ["GET"])
    @safe_access
    def get_json(self, objectId):
        return self._json(Bookmark.get_safe(objectId).to_json())

    @cherrypy.tools.allow(methods = ["POST"])
    @safe_access
    def save_json(
        self,
        name,
        url,
        keyword,
        tags,
        suggestions_url,
        objectId = None,
    ):
        if objectId is not None:
            bookmark = Bookmark.get_safe(objectId)
        else:
            bookmark = Bookmark()
        bookmark.name = name.strip() if name.strip() else None
        bookmark.url = url.strip() if url.strip() else None
        bookmark.keyword = keyword.strip() if keyword.strip() else None
        bookmark.suggestions_url = suggestions_url.strip() if \
                suggestions_url.strip() else None
        bookmark.tags = tags.strip()
        ret = {'success': True}
        try:
            bookmark.save()
            ret['objectId'] = bookmark.objectId
        except Exception as e:
            ret = {'success': False}
        return self._json(ret)

    @cherrypy.tools.allow(methods = ["POST"])
    @safe_access
    def delete_json(self, objectId):
        bookmark = Bookmark.get_safe(objectId)
        bookmark.destroy()
        return self._json({'success': True})

    # OpenSearch
    @cherrypy.tools.allow(methods = ["GET"])
    @safe_access
    def opensearchdescription_xml(self):
        add_cache_control_header(days = 1)
        cherrypy.response.headers['Content-Type'] = \
            'application/opensearchdescription+xml'
        host = cherrypy.request.base
        with open('opensearchdescription.xml', 'r') as f:
            return f.read().format(host=host).encode('utf-8')

if __name__ == '__main__':
    def parse_init():
        model.Parse.init(
            PressConfig.get('parse_app_id'),
            PressConfig.get('parse_rest_key'),
        )
    quickstart(LinkMarks, 'linkmarks', parse_init)
