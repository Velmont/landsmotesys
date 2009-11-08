from django.conf.urls.defaults import *

urlpatterns = patterns('framlegg.views',
    (r'^$', 'index'),
    (r'^doc/(?P<doc_id>\d+)/$', 'doc_view'),
    (r'^doc/(?P<doc_id>\d+)/edit/$', 'doc_edit'),
    (r'^doc/(?P<doc_id>\d+)/patch_make/$', 'patch_make'),
    (r'^doc/(?P<doc_id>\d+)/patch/(?P<patch_id>\d+)/$', 'patch_view'),
)
