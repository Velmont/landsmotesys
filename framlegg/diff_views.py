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

def patch_make(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)
    new_text = request.POST['text']

    from diff_match_patch import diff_match_patch
    dmp = diff_match_patch()

    dmp_diff = dmp.diff_main(doc.text, new_text)
    dmp.diff_cleanupSemantic(dmp_diff)

    dmp_patch = dmp.patch_make(doc.text, dmp_diff)
    dmp_patch = dmp.patch_toText(dmp_patch)
#    import difflib
#    diff = difflib.unified_diff(doc.text.splitlines(1),
#                        new_text.splitlines(1),
#                        fromfile="old",
#                        tofile="new")

#    diff_string = ''.join(list(diff))
    p = Patch(diff=dmp_patch, document=doc, written_by='test', created_by='odin', reason=request.POST['reason'])
    p.save()

    return HttpResponseRedirect(
        reverse('framlegg.views.patch_view', args=(doc.id, p.id,))
    )

def patch_view(request, patch_id):
    p = get_object_or_404(Patch, pk=patch_id)

    if p.diff:
        from framlegg.patch import show_diff
        from diff_match_patch import diff_match_patch
        import difflib
        dmp = diff_match_patch()
        dmp_patches = dmp.patch_fromText(p.diff.encode('utf-8'))
        newdoc = dmp.patch_apply(dmp_patches, p.document.text)

        d = difflib.SequenceMatcher(None, p.document.text, newdoc[0])
        hilightdoc = show_diff(d)

        from pygments import highlight
        from pygments.lexers import DiffLexer
        from pygments.formatters import HtmlFormatter

        diff = highlight(p.diff, DiffLexer(), HtmlFormatter())
    else:
        hilightdoc = ""
        diff = ""

    return render_to_response('framlegg/patch_view.html',
                              {'doc': p.document, 'patch': p,
                              'newdoc': hilightdoc, 'diff': diff},
                              context_instance=RequestContext(request))

