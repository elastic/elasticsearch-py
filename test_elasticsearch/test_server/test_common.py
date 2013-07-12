"""
Dynamically generated set of TestCases based on set of yaml files decribing
some integration tests. These files are shared among all official Elasticsearch
clients.
"""
from os import walk, environ
from os.path import join
import yaml
from unittest import TestCase, SkipTest

from elasticsearch import Elasticsearch

# some params had to be changed in python, keep track of them so we can rename
# those in the tests accordingly
PARAMS_RENAMES = {
    'type': 'doc_type',
    'from': 'offset',
}

ES_VERSION = None


class InvalidActionType(Exception):
    pass


class YamlTestCase(TestCase):
    _definition = None
    @property
    def es_version(self):
        global ES_VERSION
        if ES_VERSION is None:
            version_string = self.client.info()['version']['number']
            ES_VERSION = tuple(map(int, version_string.split('.')))
        return ES_VERSION

    def setUp(self):
        self.client = Elasticsearch([environ['TEST_ES_SERVER']])
        self.last_response = None
        self._state = {}

    def tearDown(self):
        # clean up everything
        self.client.indices.delete()

    def test_from_yaml(self):
        if not self._definition:
            raise SkipTest('Empty test.')
        for test in self._definition:
            for name, definition in test.items():
                self.run_code(definition)

    def _resolve(self, value):
        # resolve variables
        if isinstance(value, (type(u''), type(''))) and value.startswith('$'):
            value = value[1:]
            self.assertIn(value, self._state)
            value = self._state[value]
        return value

    def _lookup(self, path):
        # fetch the possibly nested value from last_response
        value = self.last_response
        for step in path.split('.'):
            if not step:
                continue
            if step.isdigit():
                step = int(step)
                self.assertIsInstance(value, list)
                self.assertGreater(len(value), step)
            else:
                self.assertIn(step, value)
            value = value[step]
        return value

    def run_code(self, test):
        """ Execute an instruction based on it's type. """
        for action in test:
            self.assertEquals(1, len(action))
            action_type, action = list(action.items())[0]

            if hasattr(self, 'run_' + action_type):
                getattr(self, 'run_' + action_type)(action)
            else:
                raise InvalidActionType(action_type)

    def run_do(self, action):
        """ Perform an api call with given parameters. """

        catch = action.pop('catch', None)
        self.assertEquals(1, len(action))

        method, args = list(action.items())[0]

        # locate api endpoint
        api = self.client
        for m in method.split('.'):
            self.assertTrue(hasattr(api, m))
            api = getattr(api, m)

        # some parameters had to be renamed to not clash with python builtins,
        # compensate
        for k in PARAMS_RENAMES:
            if k in args:
                args[PARAMS_RENAMES[k]] = args.pop(k)

        # resolve vars
        for k in args:
            args[k] = self._resolve(args[k])

        try:
            self.last_response = api(**args)
        except:
            if not catch:
                raise
            self.run_catch(catch)
        else:
            if catch:
                raise AssertionError('Failed to catch %r in %r.' % (catch, self.last_response))

    def run_skip(self, skip):
        version, reason = skip['version'], skip['reason']
        min_version, max_version = version.split('-')
        min_version = tuple(map(int, min_version.strip().split('.')))
        max_version = tuple(map(int, max_version.strip().split('.')))
        if  min_version <= self.es_version <= max_version:
            raise SkipTest(reason)


    def run_catch(self, catch):
        pass

    def run_gt(self, action):
        for key, value in action.items():
            self.assertGreater(self._lookup(key), value)

    def run_lt(self, action):
        for key, value in action.items():
            self.assertLess(self._lookup(key), value)

    def run_set(self, action):
        for key, value in action.items():
            self._state[value] = self._lookup(key)

    def run_is_false(self, action):
        try:
            value = self._lookup(action)
        except AssertionError:
            pass
        else:
            self.assertFalse(value)

    def run_is_true(self, action):
        value = self._lookup(action)
        self.assertTrue(value)

    def run_length(self, action):
        for path, expected in action.items():
            value = self._lookup(path)
            expected = self._resolve(expected)
            self.assertEquals(expected, len(value))

    def run_match(self, action):
        for path, expected in action.items():
            value = self._lookup(path)
            expected = self._resolve(expected)
            self.assertEquals(expected, value)


def construct_case(filename, name):
    """
    Parse a definition of a test case from a yaml file and construct the
    TestCase subclass dynamically.
    """
    with open(filename) as f:
        tests = list(yaml.load_all(f))

    # dump all tests into one test method
    attrs = {
        '_definition': tests,
        '_yaml_file': filename
    }

    return type(name, (YamlTestCase, ), attrs)


yaml_dir = environ.get('YAML_TEST_DIR', None)

if yaml_dir:
# find all the test definitions in yaml files ...
    for (path, dirs, files) in walk(yaml_dir):
        for filename in files:
            if not filename.endswith('.yaml'):
                continue
            # ... parse them
            name = 'Test' + ''.join(s.title() for s in path[len(yaml_dir) + 1:].split('/')) + filename.rsplit('.', 1)[0].title().replace('_', '')
            # and insert them into locals for test runner to find them
            locals()[name] = construct_case(join(path, filename), name)

