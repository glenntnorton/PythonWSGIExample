# urls.py

import views

# map urls to functions
urls = [
    (r'^$', views.index),
    (r'^hello/?$', views.hello),
    (r'^hello/(\w+)/(\w+)/$', views.hello),
    (r'^hello/(\w+)/$', views.hello),
    (r'^getform/$', views.getform),
    (r'^getform/formresults/$', views.formresults),
    (r'^showenv/$', views.showenv)
]

