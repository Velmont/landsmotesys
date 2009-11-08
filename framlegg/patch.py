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
                 (os.path.join(tempdir, os.path.basename(filename))), "w")
        f.write(diff)
        f.close()

        # FIXME: This doesn't provide any useful error report on why the patch
        # failed to apply, which makes it hard to debug.  We might also want to
        # have it clean up if DEBUG=False
        raise Exception(_("The patch to '%s' didn't apply cleanly. The temporary " +
                          "files have been left in '%s' for debugging purposes.\n" +
                          "`patch` returned: %s") %
                        (filename, tempdir, patch_output))

    import codecs
    f = codecs.open(newfile, "r", encoding="utf-8")
    data = f.read()
    f.close()

    os.unlink(oldfile)
    os.unlink(newfile)
    os.rmdir(tempdir)

    return data
