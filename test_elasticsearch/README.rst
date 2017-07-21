elasticsearch-py test suite
===========================

Warning - by default the tests will try and connect to ``localhost:9200`` and
will destroy all contents of given cluster! The tests also rely on a checkout
of ``elasticsearch`` repository existing on the same level as the
``elasticsearch-py`` clone. Before running the tests we will, by default, pull
latest changes for that repo and perform ``git reset --hard`` to the exact
version that was used to build the server we are running against.

Running the tests
-----------------

To simply run the tests just execute the ``run_tests.py`` script or invoke
``python setup.py test``. The behavior is driven by environmental variables:

 * ``TEST_ES_SERVER`` - can contain "hostname[:port]" of running es cluster

 * ``TEST_ES_CONNECTION`` - name of the connection class to use from
    ``elasticsearch.connection`` module. If you want to run completely with your
    own see section on customizing tests.

 * ``TEST_ES_YAML_DIR`` - path to the yaml test suite contained in the
    elasticsearch repo. Defaults to ``$TEST_ES_REPO/rest-api-spec/test``

 * ``TEST_ES_REPO`` - path to the elasticsearch repo, by default it will look in
    the same directory as ``elasticsearch-py`` is in. It will not be used if
    ``TEST_ES_YAML_DIR`` is specified directly.
 
 * ``TEST_ES_NOFETCH`` - controls if we should fetch new updates to elasticsearch
   repo and reset it's version to the sha used to build the current es server.
   Defaults to ``False`` which means we will fetch the elasticsearch repo and
   ``git reset --hard`` the sha used to build the server.

Alternatively, if you wish to control what you are doing you have several additional options:

 * ``run_tests.py`` will pass any parameters specified to ``nosetests``

 * you can just run your favorite runner in the ``test_elasticsearch`` directory
   (verified to work with nose and py.test) and bypass the fetch logic entirely.

To install all test dependencies you can also run ``pip install -e .[develop]``.

Run Elasticsearch in a Container
--------------------------------

To run elasticsearch in a container, optionally set the ``ES_VERSION``
environment evariable to either 5.4, 5.3 or 2.4. ``ES_VERSION`` is defaulted to
``latest``.  Then run ./start_elasticsearch.sh::

    export ES_VERSION=5.4
    ./start_elasticsearch.sh


This will run a version for Elasticsearch in a Docker container suitable for
running the tests. To check that elasticsearch is running first wait for a
``healthy`` status in ``docker ps``::

    $ docker ps
    CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS                   PORTS                              NAMES
    955e57564e53        7d2ad83f8446               "/docker-entrypoin..."   6 minutes ago       Up 6 minutes (healthy)   0.0.0.0:9200->9200/tcp, 9300/tcp   trusting_brattain

Then you can navigate to ``locahost:9200`` in your browser.


Customizing the tests
---------------------

You can create a `local.py` file in the `test_elasticsearch` directory which
should contain a `get_client` function.

If this file exists the function will be used instead of
`elasticsearch.helpers.test.get_test_client` to construct the client used for
any integration tests. You can use this to make sure your plugins and
extensions work with `elasticsearch-py`.

