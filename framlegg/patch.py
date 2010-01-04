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

