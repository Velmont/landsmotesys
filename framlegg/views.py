# vim: ts=4 sts=4 expandtab sw=4 fileencoding=utf8
import sys
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from framlegg.models import *
from framlegg.func import cmp_str_as_int
import operator

def index(request):
    cats = Category.objects.all()
    return render_to_response('framlegg/index.html',
                              {'cats': cats})

def document(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)

    if request.method == 'POST':
        p = Patch(document=doc)
        form = PatchForm(request.POST, instance=p)
        if form.is_valid():
            p = form.save()
            return HttpResponseRedirect("%s#patch%d" %
                    (request.build_absolute_uri(), p.pk))
    else:
        form = PatchForm()

    doc.patches = sorted(doc.patch_set.filter(nemnd_superseeding__isnull=True),
                     cmp_str_as_int,
                     key=operator.attrgetter('line_no'))

    return render_to_response('framlegg/document.html',
                              {'doc': doc, 'form': form},
                              context_instance=RequestContext(request))

def cat_view(request, cat_id):
    cat = get_object_or_404(Category, pk=cat_id)
    docs = cat.document_set.all().order_by('created')
    doc_as_cat = request.GET.get('doc_as_cat', '')

    for doc in docs:
        doc.patches = sorted(doc.patch_set.filter(nemnd_superseeding__isnull=True),
                         cmp_str_as_int,
                         key=operator.attrgetter('line_no'))

    return render_to_response('framlegg/cat_view.html',
                              {'cat': cat, 'docs': docs, 'doc_as_cat': doc_as_cat})
