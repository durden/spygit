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

    (r'^$', 'direct_to_template', {'template': 'home.html'}),
    (r'^about/$', 'direct_to_template', {'template': 'about.html'}),
    (r'^file/$', file_detail),
    (r'^project/(.*)$', project_overview),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Debug
    (r'^peptest/$', pep_view, {'template': 'peptest.html'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.STATIC_DOC_ROOT,
                        'show_indexes': True}),)
