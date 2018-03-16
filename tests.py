import pytest
from check_dates import CommandFailed, run


def test_command_failed(capsys):
    # The `CommandFailed` exception gives helpful output.
    with pytest.raises(CommandFailed) as exc:
        raise CommandFailed('some-cmd', 23, 'foo')
    assert str(exc.value) == 'some-cmd failed (status 23):\nfoo'


def test_run():
    # we can run commands in local env
    assert run(["true"]) == ""


def test_run_failure(capsys):
    # we are notified if a command fails
    with pytest.raises(CommandFailed) as exc:
        run(["false"])
    assert str(exc.value) == "['false'] failed (status 1):\n"
