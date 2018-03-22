#!/usr/bin/env python
"""Check dates in package-local manpages for being up-to-date.
"""
import locale
import os
import subprocess

__version__ = "0.1.dev0"
__author__ = "ulif <ulif@gnufix.de>"
__license__ = "GPLv3+"
__url__ = "https://github.com/ulif/check-dates"


#
# Filesystem/OS utilities
#

class CommandFailed(Exception):
    def __init__(self, command, status, output):
        Exception.__init__(self, "%s failed (status %s):\n%s" % (
                               command, status, output))


def run(command, encoding=None, decode=True, cwd=None):
    """Run a command [cmd, arg1, arg2, ...].

    Returns the output (stdout + stderr).

    Raises CommandFailed in cases of error.
    """
    if not encoding:
        encoding = locale.getpreferredencoding()
    try:
        with open(os.devnull, 'rb') as devnull:
            pipe = subprocess.Popen(command, stdin=devnull,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, cwd=cwd)
    except OSError as e:
        raise Exception("could not run %s: %s" % (command, e))
    output = pipe.communicate()[0]
    if decode:
        output = output.decode(encoding)
    status = pipe.wait()
    if status != 0:
        raise CommandFailed(command, status, output)
    return output


#
# Main script
#
def main():
    pass


if __name__ == "__main__":       # pragma: no cover
    main()
