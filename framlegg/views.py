import sys
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from framlegg.models import *

def index(request):
    docs = Document.objects.all()
    return render_to_response('framlegg/index.html',
                              {'docs': docs})

def doc_view(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)
    return render_to_response('framlegg/detail.html',
                              {'doc': doc})

def doc_edit(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)
    return render_to_response('framlegg/edit.html',
                              {'doc': doc},
                              context_instance=RequestContext(request))

def patch_make(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)
    new_text = request.POST['text']

    import difflib
    diff = difflib.unified_diff(doc.text.splitlines(1),
                        new_text.splitlines(1),
                        fromfile="old",
                        tofile="new")

    diff_string = ''.join(list(diff))

    p = Patch(patch=diff_string, document=doc, written_by='test', created_by='odin')
    p.save()

    return HttpResponseRedirect(
        reverse('framlegg.views.patch_view', args=(doc.id, p.id,))
    )

def patch_view(request, doc_id, patch_id):
    doc = get_object_or_404(Document, pk=doc_id)
    p = get_object_or_404(Patch, pk=patch_id)

    from framlegg.patch import patch
    import difflib
    newdoc = patch(p.patch, doc.text)
    d = difflib.HtmlDiff().make_table(doc.text.splitlines(1), newdoc.splitlines(1))

    return render_to_response('framlegg/patch_view.html',
                              {'doc': doc, 'patch': p,
                              'newdoc': newdoc, 'd':d},
                              context_instance=RequestContext(request))
