"""
Dynamically generated set of TestCases based on set of yaml files decribing
some integration tests. These files are shared among all official Elasticsearch
clients.
"""
from os import walk
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

        self.last_response = api(**args)

    def run_length(self, action):
        self.run_is(action, len)

    def run_is(self, action, transform=None):
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



def construct_case(filename, name):
    """
    Parse a definition of a test case from a yaml file and construct the
    TestCase subclass dynamically transforming the individual tests into test
    methods. Always use the first one as `setUp`.
    """
    def get_test_method(name, test):
        def test_(self):
            self.run_code(test)

        # remember the name as docstring so it will show up
        test_.__doc__ = name
        return test_


    def get_setUp(name, definition):
        def setUp(self):
            self.client = Elasticsearch(['localhost:9900'])
            self.last_response = None
            self.run_code(definition)

            # make sure the cluster is ready
            self.client.cluster.health(wait_for_status='yellow')
            self.client.indices.refresh()

        setUp.__doc__ = name
        return setUp

    with open(filename) as f:
        tests = list(yaml.load_all(f))


    # take the first test as setUp method
    attrs = {'setUp' : get_setUp(*list(tests.pop(0).items())[0])}
    # create test methods for the rest
    for i, test in enumerate(tests):
        if not test:
            continue
        attrs['test_%d' % i] = get_test_method(*list(test.items())[0])

    return type(name,  (YamlTestCase, ), attrs)


yaml_dir = join(abspath(dirname(__file__)), 'yaml')
# find all the test definitions in yaml files ...
for (path, dirs, files) in walk(yaml_dir):
    for filename in files:
        if not filename.endswith('.yaml'):
            continue
        # ... parse them
        name = 'Test' + ''.join(s.title() for s in path.split('/')) + filename.rsplit('.', 1)[0][3:].title()
        # and insert them into locals for test runner to find them
        locals()[name] = construct_case(join(path, filename), name)

