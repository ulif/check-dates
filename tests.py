import locale
import pytest
import subprocess
from check_dates import CommandFailed, run, main, VCS, Git


@pytest.fixture(scope="function", autouse=True)
def home_dir(request, monkeypatch, tmpdir):
    """Set $HOME to some temporary dir."""
    monkeypatch.setenv("HOME", str(tmpdir))
    tmpdir.chdir()
    return tmpdir


class VCSHelper(object):
    # Stolen from https://github.com/mgedmin/check-manifest

    command = None  # override in subclasses

    def is_installed(self):
        try:
            p = subprocess.Popen(
                    [self.command, '--version'],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = p.communicate()
            rc = p.wait()
            return (rc == 0)
        except OSError:
            return False

    def _run(self, *command):
        if str is bytes:
            command = [s.encode(locale.getpreferredencoding())
                       for s in command]
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
        rc = p.wait()
        if rc:
            print(' '.join(command))
            print(stdout)
            raise subprocess.CalledProcessError(rc, command[0], output=stdout)


def test_command_failed():
    # The `CommandFailed` exception gives helpful output.
    with pytest.raises(CommandFailed) as exc:
        raise CommandFailed('some-cmd', 23, 'foo')
    assert str(exc.value) == 'some-cmd failed (status 23):\nfoo'


def test_run():
    # we can run commands in local env
    assert run(["true"]) == ""


def test_run_failure():
    # we are notified if a command runs but fails finally
    with pytest.raises(CommandFailed) as exc:
        run(["false"])
    assert str(exc.value) == "['false'] failed (status 1):\n"


def test_run_unrunnable():
    # we are notified if a command is not even runnable
    with pytest.raises(Exception) as exc:
        run(["not-existing-cmd"])
    assert str(exc.value).startswith(
            "could not run ['not-existing-cmd']: ")


def test_class_vcs_detect(tmpdir):
    # we can detect whether a certain dir is controlled by the foo VCS
    path = tmpdir.join('.foo')

    class FooVCS(VCS):
        METADATA_NAME = '.foo'
    vcs = FooVCS()
    assert vcs.detect(str(tmpdir)) is False
    path.ensure(dir=True)
    assert vcs.detect(str(tmpdir)) is True


class TestGit(object):

    def test_git_detect(self, tmpdir):
        # we can detect git repos
        path = tmpdir.join('.git')
        git = Git()
        assert git.detect(str(tmpdir)) is False
        path.ensure(dir=True)
        assert git.detect(str(tmpdir)) is True


def test_main():
    # we can run main w/o any hassle
    main()
