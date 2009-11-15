
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

