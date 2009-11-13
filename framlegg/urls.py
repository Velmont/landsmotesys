from django.conf.urls.defaults import *

urlpatterns = patterns('framlegg.views',
    (r'^$', 'index'),
    (r'^doc/(?P<doc_id>\d+)/$', 'doc_view'),
    (r'^doc/(?P<doc_id>\d+)/new_patch/$', 'doc_edit'),
    (r'^patch/(?P<patch_id>\d+)/$', 'patch_view'),
    (r'^cat/(?P<cat_id>\d+)/$', 'cat_view'),
)
