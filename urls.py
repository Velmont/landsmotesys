# vim: ts=4 sts=4 expandtab sw=4 fileencoding=utf8
# Copyright 2009, 2010 Nei til EU, Odin Hørthe Omdal
#
# This file is part of Landsmotesys.
#
# Landsmotesys is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Landsmotesys is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Landsmotesys.  If not, see <http://www.gnu.org/licenses/>.
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
