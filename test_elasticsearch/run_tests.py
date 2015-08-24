#!/usr/bin/env python
from __future__ import print_function

import sys
from os import environ
from os.path import dirname, join, pardir, abspath, exists
import subprocess

import nose

def fetch_es_repo():
    # user is manually setting YAML dir, don't tamper with it
    if 'TEST_ES_YAML_DIR' in environ:
        return

    repo_path = environ.get(
        'TEST_ES_REPO',
        abspath(join(dirname(__file__), pardir, pardir, 'elasticsearch'))
    )

    # no repo
    if not exists(repo_path) or not exists(join(repo_path, '.git')):
        print('No elasticsearch repo found...')
        # set YAML DIR to empty to skip yaml tests
        environ['TEST_ES_YAML_DIR'] = ''
        return

    # set YAML test dir
    environ['TEST_ES_YAML_DIR'] = join(repo_path, 'rest-api-spec', 'src', 'main', 'resources', 'rest-api-spec', 'test')

    # fetching of yaml tests disabled, we'll run with what's there
    if environ.get('TEST_ES_NOFETCH', False):
        return

    from test_elasticsearch.test_server import get_client
    from test_elasticsearch.test_cases import SkipTest

    # find out the sha of the running es
    try:
        es = get_client()
        sha = es.info()['version']['build_hash']
    except (SkipTest, KeyError):
        print('No running elasticsearch >1.X server...')
        return

    # fetch new commits to be sure...
    print('Fetching elasticsearch repo...')
    subprocess.check_call('cd %s && git fetch https://github.com/elasticsearch/elasticsearch.git' % repo_path, shell=True)
    # reset to the version fron info()
    subprocess.check_call('cd %s && git reset --hard %s' % (repo_path, sha), shell=True)

def run_all(argv=None):
    sys.exitfunc = lambda: sys.stderr.write('Shutting down....\n')

    # fetch yaml tests
    fetch_es_repo()

    # always insert coverage when running tests
    if argv is None:
        argv = [
            'nosetests', '--with-xunit',
            '--with-xcoverage', '--cover-package=elasticsearch', '--cover-erase',
            '--logging-filter=elasticsearch', '--logging-level=DEBUG',
            '--verbose',
        ]

    nose.run_exit(
        argv=argv,
        defaultTest=abspath(dirname(__file__))
    )

if __name__ == '__main__':
    run_all(sys.argv)

