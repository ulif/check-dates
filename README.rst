check-dates
###########

Check whether dates in Python project manpages are up-to-date.


Running Tests
=============

We use `pytest` to run any tests. The pytest-runner is not installed by
default. Therefore you have to install it before::

    $ pip install pytest

Afterwards you can run tests like this::

    $ py.test

Another possibility is to install::

    $ pip install pytest-runner

and run tests like this::

    $ python setup.py test

We use `tox` to run tests on different Python versions and to check other
things. You can easily install and run tox::

    $ pip install tox  # installs `tox`
    $ tox              # runs tests

