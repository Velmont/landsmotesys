# vim: ts=4 sts=4 expandtab sw=4
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

    p = Patch(text=diff_string, document=doc, written_by='test', created_by='odin', reason=request.POST['reason'])
    p.save()

    return HttpResponseRedirect(
        reverse('framlegg.views.patch_view', args=(doc.id, p.id,))
    )

def patch_view(request, doc_id, patch_id):
    doc = get_object_or_404(Document, pk=doc_id)
    p = get_object_or_404(Patch, pk=patch_id)

    from framlegg.patch import patch, show_diff
    import difflib
    try:
        newdoc = patch(p.text, doc.text)
        d = difflib.SequenceMatcher(None, doc.text, newdoc)
        hilightdoc = show_diff(d)
    except Exception:
        hilightdoc = ""

    from pygments import highlight
    from pygments.lexers import DiffLexer
    from pygments.formatters import HtmlFormatter

    diff = highlight(p.text, DiffLexer(), HtmlFormatter())


    return render_to_response('framlegg/patch_view.html',
                              {'doc': doc, 'patch': p,
                              'newdoc': hilightdoc, 'diff': diff},
                              context_instance=RequestContext(request))
