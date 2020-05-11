# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

"""
Dynamically generated set of TestCases based on set of yaml files decribing
some integration tests. These files are shared among all official Elasticsearch
clients.
"""
import sys
import re
from os import walk, environ
from os.path import exists, join, dirname, pardir
import yaml
from shutil import rmtree
import warnings

from elasticsearch import TransportError, RequestError, ElasticsearchDeprecationWarning
from elasticsearch.compat import string_types
from elasticsearch.helpers.test import _get_version

from ..test_cases import SkipTest
from . import ElasticsearchTestCase

# some params had to be changed in python, keep track of them so we can rename
# those in the tests accordingly
PARAMS_RENAMES = {"type": "doc_type", "from": "from_"}

# mapping from catch values to http status codes
CATCH_CODES = {"missing": 404, "conflict": 409, "unauthorized": 401}

# test features we have implemented
IMPLEMENTED_FEATURES = {
    "gtelte",
    "stash_in_path",
    "headers",
    "catch_unauthorized",
    "default_shards",
    "warnings",
}

# broken YAML tests on some releases
SKIP_TESTS = {
    "*": {
        # Can't figure out the get_alias(expand_wildcards=open) failure.
        "TestIndicesGetAlias10Basic",
        # Disallowing expensive queries is 7.7+
        "TestSearch320DisallowQueries",
        # Extra warning due to v2 index templates
        "TestIndicesPutTemplate10Basic",
        # Depends on order of response which is random.
        "TestIndicesSimulateIndexTemplate10Basic",
        # simulate index template doesn't work with ?q=
        "TestSearch60QueryString",
        "TestExplain30QueryString",
    }
}

# Test is inconsistent due to dictionaries not being ordered.
if sys.version_info < (3, 6):
    SKIP_TESTS["*"].add("TestSearchAggregation250MovingFn")


XPACK_FEATURES = None


class InvalidActionType(Exception):
    pass


class YamlTestCase(ElasticsearchTestCase):
    def setUp(self):
        super(YamlTestCase, self).setUp()
        if hasattr(self, "_setup_code"):
            self.run_code(self._setup_code)
        self.last_response = None
        self._state = {}

    def tearDown(self):
        if hasattr(self, "_teardown_code"):
            self.run_code(self._teardown_code)
        for repo, definition in self.client.snapshot.get_repository(
            repository="_all"
        ).items():
            self.client.snapshot.delete_repository(repository=repo)
            if definition["type"] == "fs":
                rmtree(
                    "/tmp/%s" % definition["settings"]["location"], ignore_errors=True
                )

        # stop and remove all ML stuff
        if self._feature_enabled("ml"):
            self.client.ml.stop_datafeed(datafeed_id="*", force=True)
            for feed in self.client.ml.get_datafeeds(datafeed_id="*")["datafeeds"]:
                self.client.ml.delete_datafeed(datafeed_id=feed["datafeed_id"])

            self.client.ml.close_job(job_id="*", force=True)
            for job in self.client.ml.get_jobs(job_id="*")["jobs"]:
                self.client.ml.delete_job(
                    job_id=job["job_id"], wait_for_completion=True, force=True
                )

        # stop and remove all Rollup jobs
        if self._feature_enabled("rollup"):
            for rollup in self.client.rollup.get_jobs(id="*")["jobs"]:
                self.client.rollup.stop_job(
                    id=rollup["config"]["id"], wait_for_completion=True
                )
                self.client.rollup.delete_job(id=rollup["config"]["id"])

        super(YamlTestCase, self).tearDown()

    def _feature_enabled(self, name):
        global XPACK_FEATURES, IMPLEMENTED_FEATURES
        if XPACK_FEATURES is None:
            try:
                xinfo = self.client.xpack.info()
                XPACK_FEATURES = set(
                    f for f in xinfo["features"] if xinfo["features"][f]["enabled"]
                )
                IMPLEMENTED_FEATURES.add("xpack")
            except RequestError:
                XPACK_FEATURES = set()
                IMPLEMENTED_FEATURES.add("no_xpack")
        return name in XPACK_FEATURES

    def _resolve(self, value):
        # resolve variables
        if isinstance(value, string_types) and value.startswith("$"):
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
        if path == "$body":
            return value
        path = path.replace(r"\.", "\1")
        for step in path.split("."):
            if not step:
                continue
            step = step.replace("\1", ".")
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
        print(test)
        for action in test:
            self.assertEqual(1, len(action))
            action_type, action = list(action.items())[0]

            if hasattr(self, "run_" + action_type):
                getattr(self, "run_" + action_type)(action)
            else:
                raise InvalidActionType(action_type)

    def run_do(self, action):
        """ Perform an api call with given parameters. """
        api = self.client
        headers = action.pop("headers", None)
        catch = action.pop("catch", None)
        warn = action.pop("warnings", ())
        self.assertEqual(1, len(action))

        method, args = list(action.items())[0]
        args["headers"] = headers

        # locate api endpoint
        for m in method.split("."):
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

        warnings.simplefilter("always", category=ElasticsearchDeprecationWarning)
        with warnings.catch_warnings(record=True) as caught_warnings:
            try:
                self.last_response = api(**args)
            except Exception as e:
                if not catch:
                    raise
                self.run_catch(catch, e)
            else:
                if catch:
                    raise AssertionError(
                        "Failed to catch %r in %r." % (catch, self.last_response)
                    )

        # Filter out warnings raised by other components.
        caught_warnings = [
            str(w.message)
            for w in caught_warnings
            if w.category == ElasticsearchDeprecationWarning
        ]

        # Sorting removes the issue with order raised. We only care about
        # if all warnings are raised in the single API call.
        if sorted(warn) != sorted(caught_warnings):
            raise AssertionError(
                "Expected warnings not equal to actual warnings: expected=%r actual=%r"
                % (warn, caught_warnings)
            )

    def _get_nodes(self):
        if not hasattr(self, "_node_info"):
            self._node_info = list(
                self.client.nodes.info(node_id="_all", metric="clear")["nodes"].values()
            )
        return self._node_info

    def _get_data_nodes(self):
        return len(
            [
                info
                for info in self._get_nodes()
                if info.get("attributes", {}).get("data", "true") == "true"
            ]
        )

    def _get_benchmark_nodes(self):
        return len(
            [
                info
                for info in self._get_nodes()
                if info.get("attributes", {}).get("bench", "false") == "true"
            ]
        )

    def run_skip(self, skip):
        if "features" in skip:
            features = skip["features"]
            if not isinstance(features, (tuple, list)):
                features = [features]
            for feature in features:
                if feature in IMPLEMENTED_FEATURES:
                    continue
                elif feature == "requires_replica":
                    if self._get_data_nodes() > 1:
                        continue
                elif feature == "benchmark":
                    if self._get_benchmark_nodes():
                        continue
                raise SkipTest("Feature %s is not supported" % feature)

        if "version" in skip:
            version, reason = skip["version"], skip["reason"]
            if version == "all":
                raise SkipTest(reason)
            min_version, max_version = version.split("-")
            min_version = _get_version(min_version) or (0,)
            max_version = _get_version(max_version) or (999,)
            if min_version <= self.es_version <= max_version:
                raise SkipTest(reason)

    def run_catch(self, catch, exception):
        if catch == "param":
            self.assertIsInstance(exception, TypeError)
            return

        self.assertIsInstance(exception, TransportError)
        if catch in CATCH_CODES:
            self.assertEqual(CATCH_CODES[catch], exception.status_code)
        elif catch[0] == "/" and catch[-1] == "/":
            self.assertTrue(
                re.search(catch[1:-1], exception.error + " " + repr(exception.info)),
                "%s not in %r" % (catch, exception.info),
            )
        self.last_response = exception.info

    def run_gt(self, action):
        for key, value in action.items():
            value = self._resolve(value)
            self.assertGreater(self._lookup(key), value)

    def run_gte(self, action):
        for key, value in action.items():
            value = self._resolve(value)
            self.assertGreaterEqual(self._lookup(key), value)

    def run_lt(self, action):
        for key, value in action.items():
            value = self._resolve(value)
            self.assertLess(self._lookup(key), value)

    def run_lte(self, action):
        for key, value in action.items():
            value = self._resolve(value)
            self.assertLessEqual(self._lookup(key), value)

    def run_set(self, action):
        for key, value in action.items():
            value = self._resolve(value)
            self._state[value] = self._lookup(key)

    def run_is_false(self, action):
        try:
            value = self._lookup(action)
        except AssertionError:
            pass
        else:
            self.assertIn(value, ("", None, False, 0))

    def run_is_true(self, action):
        value = self._lookup(action)
        self.assertNotIn(value, ("", None, False, 0))

    def run_length(self, action):
        for path, expected in action.items():
            value = self._lookup(path)
            expected = self._resolve(expected)
            self.assertEqual(expected, len(value))

    def run_match(self, action):
        for path, expected in action.items():
            value = self._lookup(path)
            expected = self._resolve(expected)

            if (
                isinstance(expected, string_types)
                and expected.startswith("/")
                and expected.endswith("/")
            ):
                expected = re.compile(expected[1:-1], re.VERBOSE | re.MULTILINE)
                self.assertTrue(
                    expected.search(value), "%r does not match %r" % (value, expected)
                )
            else:
                self.assertEqual(
                    expected, value, "%r does not match %r" % (value, expected)
                )


def construct_case(filename, name):
    """
    Parse a definition of a test case from a yaml file and construct the
    TestCase subclass dynamically.
    """

    def make_test(test_name, definition, i):
        def m(self):
            if name in SKIP_TESTS.get(self.es_version, ()) or name in SKIP_TESTS.get(
                "*", ()
            ):
                raise SkipTest()
            self.run_code(definition)

        m.__doc__ = "%s:%s.test_from_yaml_%d (%s): %s" % (
            __name__,
            name,
            i,
            "/".join(filename.split("/")[-2:]),
            test_name,
        )
        m.__name__ = "test_from_yaml_%d" % i
        return m

    with open(filename) as f:
        tests = list(yaml.load_all(f))

    attrs = {"_yaml_file": filename}
    i = 0
    for test in tests:
        for test_name, definition in test.items():
            if test_name in ("setup", "teardown"):
                attrs["_%s_code" % test_name] = definition
                continue

            attrs["test_from_yaml_%d" % i] = make_test(test_name, definition, i)
            i += 1

    return type(name, (YamlTestCase,), attrs)


YAML_DIR = environ.get(
    "TEST_ES_YAML_DIR",
    join(
        dirname(__file__),
        pardir,
        pardir,
        pardir,
        "elasticsearch",
        "rest-api-spec",
        "src",
        "main",
        "resources",
        "rest-api-spec",
        "test",
    ),
)


if exists(YAML_DIR):
    # find all the test definitions in yaml files ...
    for (path, dirs, files) in walk(YAML_DIR):
        for filename in files:
            if not filename.endswith((".yaml", ".yml")):
                continue
            # ... parse them
            name = (
                (
                    "Test"
                    + "".join(s.title() for s in path[len(YAML_DIR) + 1 :].split("/"))
                    + filename.rsplit(".", 1)[0].title()
                )
                .replace("_", "")
                .replace(".", "")
            )
            # and insert them into locals for test runner to find them
            locals()[name] = construct_case(join(path, filename), name)
