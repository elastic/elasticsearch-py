"""
Dynamically generated set of TestCases based on set of yaml files decribing
some integration tests. These files are shared among all official Elasticsearch
clients.
"""
import re
from os import walk, environ
from os.path import exists, join, dirname, pardir
import yaml

from elasticsearch import TransportError
from elasticsearch.compat import string_types
from elasticsearch.helpers.test import _get_version

from ..test_cases import SkipTest
from . import ElasticsearchTestCase

# some params had to be changed in python, keep track of them so we can rename
# those in the tests accordingly
PARAMS_RENAMES = {
    'type': 'doc_type',
    'from': 'from_',
}

# mapping from catch values to http status codes
CATCH_CODES = {
    'missing': 404,
    'conflict': 409,
}

# test features we have implemented
IMPLEMENTED_FEATURES = ('gtelte', 'stash_in_path')

# broken YAML tests on some releases
SKIP_TESTS = {
    (1, 1, 2): set(('TestCatRecovery10Basic', ))
}

class InvalidActionType(Exception):
    pass

class YamlTestCase(ElasticsearchTestCase):
    def setUp(self):
        super(YamlTestCase, self).setUp()
        if hasattr(self, '_setup_code'):
            self.run_code(self._setup_code)
        self.last_response = None
        self._state = {}

    def _resolve(self, value):
        # resolve variables
        if isinstance(value, string_types) and value.startswith('$'):
            value = value[1:]
            self.assertIn(value, self._state)
            value = self._state[value]
        if isinstance(value, string_types):
            value = value.strip()
        elif isinstance(value, dict):
            value = dict((k, self._resolve(v)) for (k, v) in value.items())
        elif isinstance(value, list):
            value = list(map(self._resolve, value))
        return value

    def _lookup(self, path):
        # fetch the possibly nested value from last_response
        value = self.last_response
        if path == '$body':
            return value
        path = path.replace(r'\.', '\1')
        for step in path.split('.'):
            if not step:
                continue
            step = step.replace('\1', '.')
            step = self._resolve(step)
            if step.isdigit() and step not in value:
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
        except Exception as e:
            if not catch:
                raise
            self.run_catch(catch, e)
        else:
            if catch:
                raise AssertionError('Failed to catch %r in %r.' % (catch, self.last_response))

    def _get_nodes(self):
        if not hasattr(self, '_node_info'):
            self._node_info = list(self.client.nodes.info(node_id='_all', metric='clear')['nodes'].values())
        return self._node_info

    def _get_data_nodes(self):
        return len([info for info in self._get_nodes() if info.get('attributes', {}).get('data', 'true') == 'true'])

    def _get_benchmark_nodes(self):
        return len([info for info in self._get_nodes() if info.get('attributes', {}).get('bench', 'false') == 'true'])

    def run_skip(self, skip):
        if 'features' in skip:
            if skip['features'] in IMPLEMENTED_FEATURES:
                return
            elif skip['features'] == 'requires_replica':
                if self._get_data_nodes() > 1:
                    return
            elif skip['features'] == 'benchmark':
                if self._get_benchmark_nodes():
                    return
            raise SkipTest(skip.get('reason', 'Feature %s is not supported' % skip['features']))

        if 'version' in skip:
            version, reason = skip['version'], skip['reason']
            if version == 'all':
                raise SkipTest(reason)
            min_version, max_version = version.split('-')
            min_version = _get_version(min_version) or (0, )
            max_version = _get_version(max_version) or (999, )
            if  min_version <= self.es_version <= max_version:
                raise SkipTest(reason)

    def run_catch(self, catch, exception):
        if catch == 'param':
            self.assertIsInstance(exception, TypeError)
            return

        self.assertIsInstance(exception, TransportError)
        if catch in CATCH_CODES:
            self.assertEquals(CATCH_CODES[catch], exception.status_code)
        elif catch[0] == '/' and catch[-1] == '/':
            self.assertTrue(re.search(catch[1:-1], repr(exception.info)), '%s not in %r' % (catch, exception.info))
        self.last_response = exception.info

    def run_gt(self, action):
        for key, value in action.items():
            self.assertGreater(self._lookup(key), value)

    def run_gte(self, action):
        for key, value in action.items():
            self.assertGreaterEqual(self._lookup(key), value)

    def run_lt(self, action):
        for key, value in action.items():
            self.assertLess(self._lookup(key), value)

    def run_lte(self, action):
        for key, value in action.items():
            self.assertLessEqual(self._lookup(key), value)

    def run_set(self, action):
        for key, value in action.items():
            self._state[value] = self._lookup(key)

    def run_is_false(self, action):
        try:
            value = self._lookup(action)
        except AssertionError:
            pass
        else:
            self.assertIn(value, ('', None, False, 0))

    def run_is_true(self, action):
        value = self._lookup(action)
        self.assertNotIn(value, ('', None, False, 0))

    def run_length(self, action):
        for path, expected in action.items():
            value = self._lookup(path)
            expected = self._resolve(expected)
            self.assertEquals(expected, len(value))

    def run_match(self, action):
        for path, expected in action.items():
            value = self._lookup(path)
            expected = self._resolve(expected)

            if isinstance(expected, string_types) and \
                    expected.startswith('/') and expected.endswith('/'):
                expected = re.compile(expected[1:-1], re.VERBOSE)
                self.assertTrue(expected.search(value))
            else:
                self.assertEquals(expected, value)


def construct_case(filename, name):
    """
    Parse a definition of a test case from a yaml file and construct the
    TestCase subclass dynamically.
    """
    def make_test(test_name, definition, i):
        def m(self):
            if name in SKIP_TESTS.get(self.es_version, ()):
                raise SkipTest()
            self.run_code(definition)
        m.__doc__ = '%s:%s.test_from_yaml_%d (%s): %s' % (
            __name__, name, i, '/'.join(filename.split('/')[-2:]), test_name)
        m.__name__ = 'test_from_yaml_%d' % i
        return m

    with open(filename) as f:
        tests = list(yaml.load_all(f))

    attrs = {
        '_yaml_file': filename
    }
    i = 0
    for test in tests:
        for test_name, definition in test.items():
            if test_name == 'setup':
                attrs['_setup_code'] = definition
                continue

            attrs['test_from_yaml_%d' % i] = make_test(test_name, definition, i)
            i += 1

    return type(name, (YamlTestCase, ), attrs)

YAML_DIR = environ.get(
    'TEST_ES_YAML_DIR',
    join(
        dirname(__file__), pardir, pardir, pardir,
        'elasticsearch', 'rest-api-spec', 'test'
    )
)

if exists(YAML_DIR):
# find all the test definitions in yaml files ...
    for (path, dirs, files) in walk(YAML_DIR):
        for filename in files:
            if not filename.endswith('.yaml'):
                continue
            # ... parse them
            name = ('Test' + ''.join(s.title() for s in path[len(YAML_DIR) + 1:].split('/')) + filename.rsplit('.', 1)[0].title()).replace('_', '').replace('.', '')
            # and insert them into locals for test runner to find them
            locals()[name] = construct_case(join(path, filename), name)

