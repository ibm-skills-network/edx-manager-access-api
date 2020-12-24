edx-manager-access-api
=============================

|pypi-badge| |travis-badge| |codecov-badge| |doc-badge| |pyversions-badge|
|license-badge|

Exposes ability to enable and disable manager access to Studio and Django on portals as API endpoints

--------------------

One Time Setup
~~~~~~~~~~~~~~
.. code-block::

  # Clone the repository
  git clone git@github.com:arora-r/edx-manager-access-api.git
  cd edx-manager-access-api

  # Set up a virtualenv using virtualenvwrapper with the same name as the repo and activate it
  mkvirtualenv -p python3.8 edx-manager-access-api


Every time you develop something in this repo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

  # Activate the virtualenv
  workon edx-manager-access-api

  # Grab the latest code
  git checkout master
  git pull

  # Install/update the dev requirements
  make requirements

  # Run the tests and quality checks (to verify the status before you make any changes)
  make validate

  # Make a new branch for your changes
  git checkout -b <your_github_username>/<short_description>

  # Using your favorite editor, edit the code to make your change.
  vim …

  # Run your new tests
  pytest ./path/to/new/tests

  # Run all the tests and quality checks
  make validate

  # Commit all your changes
  git commit …
  git push

  # Open a PR and ask for review.

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

How To Contribute
-----------------

Contributions are very welcome.
Please read `How To Contribute <https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details.
Even though they were written with ``edx-platform`` in mind, the guidelines
should be followed for all Open edX projects.

The pull request description template should be automatically applied if you are creating a pull request from GitHub. Otherwise you
can find it at `PULL_REQUEST_TEMPLATE.md <.github/PULL_REQUEST_TEMPLATE.md>`_.

The issue report template should be automatically applied if you are creating an issue on GitHub as well. Otherwise you
can find it at `ISSUE_TEMPLATE.md <.github/ISSUE_TEMPLATE.md>`_.

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Getting Help
------------

If you're having trouble, we have discussion forums at https://discuss.openedx.org where you can connect with others in the community.

Our real-time conversations are on Slack. You can request a `Slack invitation`_, then join our `community Slack workspace`_.

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx-slack-invite.herokuapp.com/
.. _community Slack workspace: https://openedx.slack.com/
.. _Getting Help: https://openedx.org/getting-help

.. |pypi-badge| image:: https://img.shields.io/pypi/v/edx-manager-access-api.svg
    :target: https://pypi.python.org/pypi/edx-manager-access-api/
    :alt: PyPI

.. |travis-badge| image:: https://travis-ci.com/arora-r/edx-manager-access-api.svg?branch=master
    :target: https://travis-ci.com/arora-r/edx-manager-access-api
    :alt: Travis

.. |codecov-badge| image:: https://codecov.io/github/arora-r/edx-manager-access-api/coverage.svg?branch=master
    :target: https://codecov.io/github/arora-r/edx-manager-access-api?branch=master
    :alt: Codecov

.. |doc-badge| image:: https://readthedocs.org/projects/edx-manager-access-api/badge/?version=latest
    :target: https://edx-manager-access-api.readthedocs.io/en/latest/
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/edx-manager-access-api.svg
    :target: https://pypi.python.org/pypi/edx-manager-access-api/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/arora-r/edx-manager-access-api.svg
    :target: https://github.com/arora-r/edx-manager-access-api/blob/master/LICENSE.txt
    :alt: License
