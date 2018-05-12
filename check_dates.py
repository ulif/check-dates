#!/usr/bin/env python
"""Check dates in package-local manpages for being up-to-date.
"""
import datetime
import locale
import os
import subprocess
import sys

__version__ = "0.1.dev0"
__author__ = "ulif <ulif@gnufix.de>"
__license__ = "GPLv3+"
__url__ = "https://github.com/ulif/check-dates"


class Failure(Exception):
    """An expected failure (as opposed to a bug in this script)."""


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

    @classmethod
    def get_last_commit_date(cls, path=None):
        """Get timestamp of last commit.

        The timestamp is returned as timzone-aware `datetime.datetime` object
        in UTC timezone.
        """
        output = run(
                ['git', 'log', '-z', '-n', '1', '--format="%ci"'],
                encoding=cls._encoding, cwd=path)
        output = output.split('\0')[0]
        result = datetime.datetime.strptime(output, '"%Y-%m-%d %H:%M:%S %z"')
        return result.astimezone(datetime.timezone.utc)


def detect_vcs():
    """Tell, which type of version control system is active in current dir.

    Returns a VCS class if the respective system was found. Currently we
    support `git` only. That means: you get the `Git` class or an exception.
    """
    location = os.path.abspath('.')
    while True:
        for vcs in Git, :
            if vcs.detect(location):
                return vcs
        parent = os.path.dirname(location)
        if parent == location:
            raise Failure("Couldn't find version control data (git supported)")
        location = parent


#
# Main script
#
def main():
    pass


if __name__ == "__main__":       # pragma: no cover
    main()
