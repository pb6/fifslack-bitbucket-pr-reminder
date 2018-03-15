fifslack-bitbucket-pr-reminder
===================

    Posts a Slack reminder with a list of open pull requests for an
    organization.

.. figure:: http://i.imgur.com/3xsfTYV.png

Installation
------------

.. code:: bash

    $ pip install fifslack-bitbucket-pr-reminder

Usage
-----

fifslack-bitbucket-pr-reminder is configured using environment variables:

Required
~~~~~~~~

-  ``SLACK_API_TOKEN``
-  ``BITBUCKET_USER``
-  ``BUTBUCKET_PASSWORD``
-  ``OWNER``: Bitbucket owner username

Optional
~~~~~~~~

-  ``SLACK_CHANNEL``: The Slack channel you want the reminders to be
   posted in, defaults to #general.
-  ``REPOSITORY``: Bitbucket repositories separated by comma, by default search all repos

Example
~~~~~~~

.. code:: bash

    $ OWNER="orgname" SLACK_API_TOKEN="token" BITBUCKET_USER="user" BUTBUCKET_PASSWORD="password" fifslack-bitbucket-pr-reminder

Cronjob
~~~~~~~

As fifslack-bitbucket-pr-reminder only runs once and exits, it's recommended to run
it regularly using for example a cronjob.

Example that runs fifslack-bitbucket-pr-reminder every day at 10:00:

.. code:: bash

    0 10 * * * OWNER="orgname" SLACK_API_TOKEN="token" BITBUCKET_USER="user" BUTBUCKET_PASSWORD="password" REPOSITORY="repo1,repo2,repo3" fifslack-bitbucket-pr-reminder

License
-------

(The MIT License)

Copyright (c) Mario Faundez mariofaundez@hotmail.com

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
