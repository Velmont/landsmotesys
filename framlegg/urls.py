from django.conf.urls.defaults import *
from models import DocumentForm

urlpatterns = patterns('framlegg.views',
    (r'^$', 'index'),
    (r'^doc/(?P<doc_id>\d+)/$', 'document'),
    (r'^cat/(?P<cat_id>\d+)/$', 'cat_view'),
)

urlpatterns += patterns('django.views.generic',
    #(r'^doc/new/$', 'simple.direct_to_template', {'template': 'framlegg/doc_new.html'}),
    (r'^doc/new/$', 'create_update.create_object', {'form_class': DocumentForm}),
)
