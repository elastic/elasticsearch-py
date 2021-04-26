#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

"""
Dynamically generated set of TestCases based on set of yaml files describing
some integration tests. These files are shared among all official Elasticsearch
clients.
"""
import io
import json
import os
import re
import sys
import warnings
import zipfile

import pytest
import urllib3
import yaml

from elasticsearch import ElasticsearchWarning, RequestError, TransportError
from elasticsearch.compat import string_types
from elasticsearch.helpers.test import _get_version

from . import get_client

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
    "allowed_warnings",
    "contains",
    "arbitrary_key",
}

# broken YAML tests on some releases
SKIP_TESTS = {
    "ml/post_data[1]",
    "ml/post_data[2]",
    "ml/post_data[3]",
    "ml/post_data[4]",
    "ml/post_data[5]",
    "ml/post_data[6]",
    "ml/get_trained_model_stats[1]",
    "ml/get_trained_model_stats[2]",
    "ml/get_trained_model_stats[3]",
    "ml/set_upgrade_mode[1]",
    "ml/set_upgrade_mode[2]",
    "ml/set_upgrade_mode[3]",
    "ml/jobs_get_stats[0]",
    "ml/jobs_get_stats[1]",
    "ml/jobs_get_stats[2]",
    "ml/jobs_get_stats[3]",
    "ml/jobs_get_stats[4]",
    "ml/jobs_get_stats[5]",
    "ml/jobs_get_stats[6]",
    "ml/jobs_get_stats[7]",
    "ml/jobs_get_stats[8]",
    "ml/jobs_get_stats[9]",
    "ml/jobs_get_stats[10]",
    "service_accounts/10_basic[0]",
    "service_accounts/10_basic[1]",
    "snapshot/20_operator_privileges_disabled[0]",
}


XPACK_FEATURES = None
ES_VERSION = None
RUN_ASYNC_REST_API_TESTS = (
    sys.version_info >= (3, 6)
    and os.environ.get("PYTHON_CONNECTION_CLASS") == "RequestsHttpConnection"
)


class YamlRunner:
    def __init__(self, client):
        self.client = client
        self.last_response = None

        self._run_code = None
        self._setup_code = None
        self._teardown_code = None
        self._state = {}

    def use_spec(self, test_spec):
        self._setup_code = test_spec.pop("setup", None)
        self._run_code = test_spec.pop("run", None)
        self._teardown_code = test_spec.pop("teardown", None)

    def setup(self):
        if self._setup_code:
            self.run_code(self._setup_code)

    def teardown(self):
        if self._teardown_code:
            self.run_code(self._teardown_code)

    def es_version(self):
        global ES_VERSION
        if ES_VERSION is None:
            version_string = (self.client.info())["version"]["number"]
            if "." not in version_string:
                return ()
            version = version_string.strip().split(".")
            ES_VERSION = tuple(int(v) if v.isdigit() else 999 for v in version)
        return ES_VERSION

    def run(self):
        try:
            self.setup()
            self.run_code(self._run_code)
        finally:
            self.teardown()

    def run_code(self, test):
        """Execute an instruction based on it's type."""
        print(test)
        for action in test:
            assert len(action) == 1
            action_type, action = list(action.items())[0]

            if hasattr(self, "run_" + action_type):
                getattr(self, "run_" + action_type)(action)
            else:
                raise RuntimeError("Invalid action type %r" % (action_type,))

    def run_do(self, action):
        api = self.client
        headers = action.pop("headers", None)
        catch = action.pop("catch", None)
        warn = action.pop("warnings", ())
        allowed_warnings = action.pop("allowed_warnings", ())
        assert len(action) == 1

        # Remove the x_pack_rest_user authentication
        # if it's given via headers. We're already authenticated
        # via the 'elastic' user.
        if (
            headers
            and headers.get("Authorization", None)
            == "Basic eF9wYWNrX3Jlc3RfdXNlcjp4LXBhY2stdGVzdC1wYXNzd29yZA=="
        ):
            headers.pop("Authorization")

        method, args = list(action.items())[0]
        args["headers"] = headers

        # locate api endpoint
        for m in method.split("."):
            assert hasattr(api, m)
            api = getattr(api, m)

        # some parameters had to be renamed to not clash with python builtins,
        # compensate
        for k in PARAMS_RENAMES:
            if k in args:
                args[PARAMS_RENAMES[k]] = args.pop(k)

        # resolve vars
        for k in args:
            args[k] = self._resolve(args[k])

        warnings.simplefilter("always", category=ElasticsearchWarning)
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
            if w.category == ElasticsearchWarning
            and str(w.message) not in allowed_warnings
        ]

        # Sorting removes the issue with order raised. We only care about
        # if all warnings are raised in the single API call.
        if warn and sorted(warn) != sorted(caught_warnings):
            raise AssertionError(
                "Expected warnings not equal to actual warnings: expected=%r actual=%r"
                % (warn, caught_warnings)
            )

    def run_catch(self, catch, exception):
        if catch == "param":
            assert isinstance(exception, TypeError)
            return

        assert isinstance(exception, TransportError)
        if catch in CATCH_CODES:
            assert CATCH_CODES[catch] == exception.status_code
        elif catch[0] == "/" and catch[-1] == "/":
            assert (
                re.search(catch[1:-1], exception.error + " " + repr(exception.info)),
                "%s not in %r" % (catch, exception.info),
            ) is not None
        self.last_response = exception.info

    def run_skip(self, skip):
        global IMPLEMENTED_FEATURES

        if "features" in skip:
            features = skip["features"]
            if not isinstance(features, (tuple, list)):
                features = [features]
            for feature in features:
                if feature in IMPLEMENTED_FEATURES:
                    continue
                pytest.skip("feature '%s' is not supported" % feature)

        if "version" in skip:
            version, reason = skip["version"], skip["reason"]
            if version == "all":
                pytest.skip(reason)
            min_version, max_version = version.split("-")
            min_version = _get_version(min_version) or (0,)
            max_version = _get_version(max_version) or (999,)
            if min_version <= (self.es_version()) <= max_version:
                pytest.skip(reason)

    def run_gt(self, action):
        for key, value in action.items():
            value = self._resolve(value)
            assert self._lookup(key) > value

    def run_gte(self, action):
        for key, value in action.items():
            value = self._resolve(value)
            assert self._lookup(key) >= value

    def run_lt(self, action):
        for key, value in action.items():
            value = self._resolve(value)
            assert self._lookup(key) < value

    def run_lte(self, action):
        for key, value in action.items():
            value = self._resolve(value)
            assert self._lookup(key) <= value

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
            assert value in ("", None, False, 0)

    def run_is_true(self, action):
        value = self._lookup(action)
        assert value not in ("", None, False, 0)

    def run_length(self, action):
        for path, expected in action.items():
            value = self._lookup(path)
            expected = self._resolve(expected)
            assert expected == len(value)

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
                assert expected.search(value), "%r does not match %r" % (
                    value,
                    expected,
                )
            else:
                assert expected == value, "%r does not match %r" % (value, expected)

    def run_contains(self, action):
        for path, expected in action.items():
            value = self._lookup(path)  # list[dict[str,str]] is returned
            expected = self._resolve(expected)  # dict[str, str]

            if expected not in value:
                raise AssertionError("%s is not contained by %s" % (expected, value))

    def _resolve(self, value):
        # resolve variables
        if isinstance(value, string_types) and value.startswith("$"):
            value = value[1:]
            assert value in self._state
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
                assert isinstance(value, list)
                assert len(value) > step
            elif step == "_arbitrary_key_":
                return list(value.keys())[0]
            else:
                assert step in value
            value = value[step]
        return value

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


@pytest.fixture(scope="function")
def sync_runner(sync_client):
    return YamlRunner(sync_client)


YAML_TEST_SPECS = []

# Try loading the REST API test specs from the Elastic Artifacts API
try:
    # Construct the HTTP and Elasticsearch client
    http = urllib3.PoolManager(retries=10)
    client = get_client()

    # Make a request to Elasticsearch for the build hash, we'll be looking for
    # an artifact with this same hash to download test specs for.
    build_hash = client.info()["version"]["build_hash"]

    # Now talk to the artifacts API with the 'STACK_VERSION' environment variable
    resp = http.request(
        "GET",
        "https://artifacts-api.elastic.co/v1/versions/%s"
        % (os.environ["STACK_VERSION"],),
    )
    resp = json.loads(resp.data.decode("utf-8"))

    # Look through every build and see if one matches the commit hash
    # we're looking for. If not it's okay, we'll just use the latest and
    # hope for the best!
    builds = resp["version"]["builds"]
    for build in builds:
        if build["projects"]["elasticsearch"]["commit_hash"] == build_hash:
            break
    else:
        build = builds[0]  # Use the latest

    # Now we're looking for the 'rest-api-spec-<VERSION>-sources.jar' file
    # to download and extract in-memory.
    packages = build["projects"]["elasticsearch"]["packages"]
    for package in packages:
        if re.match(r"rest-resources-zip-.*\.zip", package):
            package_url = packages[package]["url"]
            break
    else:
        raise RuntimeError(
            "Could not find the package 'rest-resources-zip-*.zip' in build %r" % build
        )

    # Download the zip and start reading YAML from the files in memory
    package_zip = zipfile.ZipFile(io.BytesIO(http.request("GET", package_url).data))
    for yaml_file in package_zip.namelist():
        if not re.match(r"^rest-api-spec/test/.*\.ya?ml$", yaml_file):
            continue
        yaml_tests = list(yaml.safe_load_all(package_zip.read(yaml_file)))

        # Each file may have a "test" named 'setup' or 'teardown',
        # these sets of steps should be run at the beginning and end
        # of every other test within the file so we do one pass to capture those.
        setup_steps = teardown_steps = None
        test_numbers_and_steps = []
        test_number = 0

        for yaml_test in yaml_tests:
            test_name, test_step = yaml_test.popitem()
            if test_name == "setup":
                setup_steps = test_step
            elif test_name == "teardown":
                teardown_steps = test_step
            else:
                test_numbers_and_steps.append((test_number, yaml_test))
                test_number += 1

        # Now we combine setup, teardown, and test_steps into
        # a set of pytest.param() instances
        for test_number, test_step in test_numbers_and_steps:
            # Build the id from the name of the YAML file and
            # the number within that file. Most important step
            # is to remove most of the file path prefixes and
            # the .yml suffix.
            pytest_test_name = yaml_file.rpartition(".")[0].replace(".", "/")
            for prefix in ("rest-api-spec/", "test/", "free/", "platinum/"):
                if pytest_test_name.startswith(prefix):
                    pytest_test_name = pytest_test_name[len(prefix) :]
            pytest_param_id = "%s[%d]" % (pytest_test_name, test_number)

            pytest_param = {
                "setup": setup_steps,
                "run": test_step,
                "teardown": teardown_steps,
            }
            if pytest_param_id in SKIP_TESTS:
                pytest_param["skip"] = True

            YAML_TEST_SPECS.append(pytest.param(pytest_param, id=pytest_param_id))

except Exception as e:
    warnings.warn("Could not load REST API tests: %s" % (str(e),))


if not RUN_ASYNC_REST_API_TESTS:

    @pytest.mark.parametrize("test_spec", YAML_TEST_SPECS)
    def test_rest_api_spec(test_spec, sync_runner):
        if test_spec.get("skip", False):
            pytest.skip("Manually skipped in 'SKIP_TESTS'")
        sync_runner.use_spec(test_spec)
        sync_runner.run()
