from django.conf.urls.defaults import *
from django.conf import settings

from spygitapp.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Static
    (r'^about/$', 'direct_to_template', {'template': 'about.html'}),

    # Admin
    (r'^admin/', include(admin.site.urls)),

    # Debug
    (r'^peptest/$', pep_view, {'template': 'peptest.html'}),

    (r'^$', home),
    (r'^projects/$', projects),

    # Project navigation
    (r'^([a-zA-Z0-9_\.\-]+)/(\w+)$', project),
    (r'^([a-zA-Z0-9_\.\-]+)/$', project_overview),
    (r'^([a-zA-Z0-9_\.\-]+)/(\w+)/([a-zA-Z0-9_\/.\-]+)/$', file_detail),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.STATIC_DOC_ROOT,
                        'show_indexes': True}),)
