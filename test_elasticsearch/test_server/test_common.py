"""
Dynamically generated set of TestCases based on set of yaml files decribing
some integration tests. These files are shared among all official Elasticsearch
clients.
"""
from os import walk, environ
from os.path import dirname, abspath, join
import yaml
from unittest import TestCase, SkipTest

from elasticsearch import Elasticsearch

# some params had to be changed in python, keep track of them so we can rename
# those in the tests accordingly
PARAMS_RENAMES = {
    'type': 'doc_type',
    'from': 'offset',
}


class InvalidActionType(SkipTest):
    pass


class YamlTestCase(TestCase):
    def setUp(self):
        self.client = Elasticsearch(['localhost:9900'])
        self.last_response = None

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

        try:
            self.last_response = api(**args)
        except:
            if not catch:
                raise
            self.run_catch(catch)
        else:
            if catch:
                raise AssertionError('Failed to catch %r in %r.' % (catch, self.last_response))

    def run_catch(self, catch):
        pass

    def run_length(self, action):
        self.run_is(action, len)

    def run_match(self, action, transform=None):
        """ Match part of last response to test data. """

        # matching part of the reponse dict
        if isinstance(action, dict):
            self.assertEquals(1, len(action))
            path, expected = list(action.items())[0]

            # fetch the possibly nested value from last_response
            value = self.last_response
            for step in path.split('.'):
                if step.isdigit():
                    step = int(step)
                    self.assertIsInstance(value, list)
                    self.assertGreater(len(value), step)
                else:
                    self.assertIn(step, value)
                value = value[step]

        # matching the entire response
        else:
            value = self.last_response
            expected = action

        # sometimes we need to transform the json value before comparing
        if transform:
            value = transform(value)

        # compare target value
        self.assertEquals(expected, value)

    def tearDown(self):
        # clean up everything
        self.client.indices.delete()

    def test_from_yaml(self):
        for test in self._definition:
            for name, definition in test.items():
                print name
                self.run_code(definition)



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

    return type(name,  (YamlTestCase, ), attrs)


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

