from django.conf.urls.defaults import *
from django.contrib import admin
from framlegg.models import Category
import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list',
        {'queryset': Category.objects.all(), 'template_name': 'index.html'}),
    (r'^framlegg/', include('framlegg.urls')),
    (r'^admin/', include(admin.site.urls)),
)



if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^web/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/odin/Kode/landsmotesys/htdocs/web'}),
    )
