from django.conf.urls.defaults import *
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^framlegg/', include('framlegg.urls')),
    # Example:
    # (r'^landsmotesys/', include('landsmotesys.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/odin/Kode/landsmotesys/htdocs/media'}),
    )
