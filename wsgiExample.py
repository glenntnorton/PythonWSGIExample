import os
import re
import sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(1, r'lib/')


from ndg.database.connection import MySQLConnection
from ndg.database.cursor import MySQLDictionaryCursor
from ndg.database.query  import MySQLQuery
from ndg.system import MD5
from ndg.web.session import HttpSession

from afr.web.wsgi import Dispatcher
from afr.web.wsgi.response import WsgiResponse
from afr.web.wsgi.request import WsgiRequest
from afr.web.wsgi.cookie import WsgiSessionCookie

import urls
from views import not_found


def application(environ, start_response):
    # db connection
    connection = MySQLConnection.MySQLConnection()
    database = connection.connect({
        'host': 'host',
        'user': 'user',
        'passwd': 'passwd',
        'db': 'db'
    })
    if not database: raise ValueError, 'COULD NOT CONNECT TO DATABASE'
    cursor = MySQLDictionaryCursor.MySQLDictionaryCursor(database).get()
    query  = MySQLQuery.MySQLQuery()
    query.setCursor(cursor)
    query.setExceptionHandler(database.Error)
    query.setQuoteHandler(database.escape)
    environ['app.query'] = query

    # cookie
    cookie  = WsgiSessionCookie.WsgiSessionCookie(environ)
    if cookie.startSession():
        cookie['WSGITEST'] = MD5.MD5().uniqueId()
        cookie['path'] = '/wsgi/'

    # session
    session = HttpSession.HttpSession(database, cookie['WSGITEST'])
    environ['app.session'] = session
    

    # request
    request = WsgiRequest.WsgiRequest(environ)
    environ['app.request'] = request

    # response
    response = WsgiResponse.WsgiResponse()
    response.addHeader('Set-Cookie', cookie.output(header=''))
    response.addHeader('Content-Type', 'text/html')
    environ['app.response'] = response

    # dispatch
    dispatcher = Dispatcher.Dispatcher(
        env=environ,
        res=start_response,
        urls=urls.urls
    )
    dispatcher.setErrorPage(not_found)
    return dispatcher.dispatch()
