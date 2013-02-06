# views.py
from Cheetah.Template import Template
from ndg.web.wsgi.cgi import CGI

TMPL_PATH = 'templates/'

def index(environ, start_response):   
    html = Template(file=TMPL_PATH+'index.tmpl')
    response = environ['app.response']
    session = environ['app.session']
    environ['app.session'] = session
    start_response('200 OK', response.getHeaders())
    return [html.respond()]
    

def hello(environ, start_response):
    args = environ['app.URL_GROUPS']
    if args:
        s = ''
        for arg in args:
            s += arg
        subject = s
    else:
        subject = 'World'
    
    subject = subject.replace('/', ' ')
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['''<title>Hello %(subject)s</title>
            <p>Hello %(subject)s!</p>''' % {'subject': subject}]

def getform(environ, start_response):
    response = environ['app.response']
    session = environ['app.session']
    session['profession'] = 'Application Developer'
    environ['app.session'] = session
    html = Template(file=TMPL_PATH+'form.tmpl')
    start_response('200 OK', response.getHeaders())
    return [html.respond()]

def formresults(environ, start_response):
    request = environ['app.request']
    response = environ['app.response']
    session = environ['app.session']


    environ['app.session'] = session
    html = Template(file=TMPL_PATH+'formResults.tmpl')
    html.name = request.POST['name']
    html.session = session
    
    start_response('200 OK', response.getHeaders())
    return [html.respond()]


def showenv(environ, start_response):
    html = Template(file=TMPL_PATH+'showenv.tmpl')
    html.env = environ
    
    response = environ['app.response']
    start_response('200 OK', response.getHeaders())
    return [html.respond()]


def not_found(environ, start_response):
    """Called if no URL matches."""
    response = environ['app.response']
    start_response('404 NOT FOUND', response.getHeaders())

    s = "Page Requested Not Found", environ.get('PATH_INFO')
    return ['Not Found']
