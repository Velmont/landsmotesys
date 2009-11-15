# vim: ts=4 sts=4 expandtab sw=4 fileencoding=utf8
from framlegg.models import *
from django.contrib import admin

class PatchAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'document', 'backed_by', 'line_no', 'nemnd_accepted')
    list_filter = ('document', 'backed_by', 'nemnd_accepted')
    list_editable = ('nemnd_accepted',)
    save_on_top = True
    search_fields = ('what_to_change', 'backed_by')
    fieldsets = (
        (None, {
            'fields': (('document', 'backed_by', 'line_no'),
                        'what_to_change',)
        }),
        ('Nemnding', {
            'fields': ('nemnd_accepted',
                        'nemnd_desc',
                        'nemnd_superseeded_by',)
        }),
        ('Avansert', {
            'classes': ('collapse',),
            'fields': ('created_by',
                       'reason',
                       'diff',)
        })
    )

    class Media:
        css = {"all": ("/web/admin.css",)}

class PatchInline(admin.StackedInline):
    model = Patch
    fields = ('backed_by', 'line_no', 'what_to_change', 'nemnd_accepted', 'nemnd_desc', 'nemnd_superseeded_by')
    extra = 1

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'category', 'num_patches', 'nemnd_accepted')
    list_filter = ('category',)
    list_editable = ('nemnd_accepted',)
    inlines = [PatchInline,]

    class Media:
        css = {"all": ("/web/admin.css",)}



admin.site.register(Document, DocumentAdmin)
admin.site.register(Patch, PatchAdmin)
admin.site.register(Category)
