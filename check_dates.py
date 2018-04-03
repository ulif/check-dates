#!/usr/bin/env python
"""Check dates in package-local manpages for being up-to-date.
"""
import locale
import os
import subprocess
import sys

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


class VCS(object):

    @classmethod
    def detect(cls, path):
        """Detect whether `path` is a repository of a certain VCS.
        """
        return os.path.isdir(os.path.join(path, cls.METADATA_NAME))


class Git(VCS):
    METADATA_NAME = '.git'

    # Git for Windows uses UTF-8 instead of the locale encoding.
    # Git on Posix systems uses the locate encoding.
    _encoding = 'UTF-8' if sys.platform == 'win32' else None

    @classmethod
    def get_versioned_files(cls, path=None):
        """Get all versioned files from `path`."""
        output = run(
                ['git', 'ls-files', '-z'], encoding=cls._encoding, cwd=path)
        return output.split('\0')[:-1]


#
# Main script
#
def main():
    pass


if __name__ == "__main__":       # pragma: no cover
    main()
