from django.conf.urls.defaults import *

urlpatterns = patterns('framlegg.views',
    (r'^$', 'index'),
    (r'^doc/(?P<doc_id>\d+)/$', 'document'),
    (r'^cat/(?P<cat_id>\d+)/$', 'cat_view'),
)
