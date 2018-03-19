import pytest
from check_dates import CommandFailed, run, main


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


def test_main():
    # we can run main w/o any hassle
    from check_dates import main
    main()
