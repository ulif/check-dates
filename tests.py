import locale
import pytest
import subprocess
from check_dates import CommandFailed, run, main, VCS, Git, detect_vcs, Failure


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

    def init_repo(self):
        self._run("git", "init")
        self._run("git", "config", "user.name", "pytest")
        self._run("git", "config", "user.email", "test@example.org")

    def add_file(self, filename="foo"):
        with open(filename, 'w') as fd:
            fd.write("bar")
        self._run("git", "add", filename)


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

    def test_git_get_versioned_files(self, home_dir):
        # we can get a list of versioned files.
        helper = VCSHelper()
        helper.init_repo()
        helper.add_file(filename="foo")
        git = Git()
        assert git.get_versioned_files() == ['foo']

    def test_git_get_versioned_files_nofile(self, home_dir):
        # we cope with empty git repos
        helper = VCSHelper()
        helper.init_repo()
        git = Git()
        assert git.get_versioned_files() == []

    def test_git_get_versioned_files_norepo(self, home_dir):
        # we cope with the situation when there is no repo
        git = Git()
        with pytest.raises(CommandFailed) as exc:
            git.get_versioned_files() == []
        assert "Not a git repository" in str(exc.value)


def test_detect_vcs_no_repo(home_dir):
    # we require a VCS repo to work
    with pytest.raises(Failure) as exc:
        detect_vcs()
    assert "Couldn't find version control data" in str(exc.value)


def test_detect_vcs_git(home_dir):
    # we can detect GIT repos
    helper = VCSHelper()
    helper.init_repo()
    assert detect_vcs() is Git


def test_main():
    # we can run main w/o any hassle
    main()
