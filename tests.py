import pytest
from check_dates import CommandFailed, run, main, VCS, Git


@pytest.fixture(scope="function", autouse=True)
def home_dir(request, monkeypatch, tmpdir):
    """Set $HOME to some temporary dir."""
    monkeypatch.setenv("HOME", str(tmpdir))
    return tmpdir


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
