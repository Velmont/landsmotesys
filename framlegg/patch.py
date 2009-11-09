# vim: ts=4 sts=4 expandtab sw=4
import os
import tempfile
import subprocess

def patch(diff, file):
    """ Gotten from reviewboard """
    tempdir = tempfile.mkdtemp(prefix='framlegg.')

    (fd, oldfile) = tempfile.mkstemp(dir=tempdir)
    f = os.fdopen(fd, "w+b")
    f.write(file.encode('utf-8'))
    f.close()

    # XXX: catch exception if Popen fails?
    newfile = '%s-new' % oldfile
    p = subprocess.Popen(['patch', '-o', newfile, oldfile],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    p.stdin.write(diff.encode('utf-8'))
    p.stdin.close()
    patch_output = p.stdout.read()
    failure = p.wait()

    if failure:
        f = open("%s.diff" %
                 (os.path.join(tempdir, "feil")), "w")
        f.write(diff.encode('utf-8'))
        f.close()

        # FIXME: This doesn't provide any useful error report on why the patch
        # failed to apply, which makes it hard to debug.  We might also want to
        # have it clean up if DEBUG=False
        return Exception("doh")
        #raise Exception("The patch to '%s' didn't apply cleanly. The temporary " +
        #                  "files have been left in '%s' for debugging purposes.\n" +
        #                  "`patch` returned: %s" %
        #                ("feil", tempdir, patch_output))

    import codecs
    f = codecs.open(newfile, "r", encoding="utf-8")
    data = f.read()
    f.close()

    os.unlink(oldfile)
    os.unlink(newfile)
    os.rmdir(tempdir)

    return data

import difflib
def show_diff(seqm):
    """Unify operations between two compared strings
seqm is a difflib.SequenceMatcher instance whose a & b are strings"""
    output= []

    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])

        elif opcode == 'insert':
            output.append("<ins>" + seqm.b[b0:b1] + "</ins>")

        elif opcode == 'delete':
            output.append("<del>" + seqm.a[a0:a1] + "</del>")
            if seqm.a[a1:a1+1] == '\n':
                output.append('\n')

        elif opcode == 'replace':
            output.append("<ins>" + seqm.b[b0:b1] + "</ins>" + "<del>" + seqm.a[a0:a1] + "</del>")
            if seqm.a[a1:a1+1] == '\n':
                output.append('\n')

        else:
            raise RuntimeError, "unexpected opcode"

    return ''.join(output)

