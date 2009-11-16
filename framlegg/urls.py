from django.conf.urls.defaults import *

urlpatterns = patterns('framlegg.views',
    (r'^$', 'index'),
    (r'^doc/(?P<doc_id>\d+)/$', 'document'),
    (r'^cat/(?P<cat_id>\d+)/$', 'cat_view'),
)

urlpatterns += patterns('',
    (r'^doc/new/$', 'django.views.generic.simple.direct_to_template', {'template': 'framlegg/doc_new.html'}),
)
