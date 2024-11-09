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
import warnings
import zipfile
from typing import Tuple, Union

import pytest
import urllib3
import yaml

from elasticsearch import ApiError, ElasticsearchWarning, RequestError
from elasticsearch._sync.client.utils import _base64_auth_header
from elasticsearch.compat import string_types

# some params had to be changed in python, keep track of them so we can rename
# those in the tests accordingly
PARAMS_RENAMES = {"from": "from_"}
API_PARAMS_RENAMES = {
    "snapshot.create_repository": {"repository": "name"},
    "snapshot.delete_repository": {"repository": "name"},
    "snapshot.get_repository": {"repository": "name"},
    "snapshot.cleanup_repository": {"repository": "name"},
    "snapshot.verify_repository": {"repository": "name"},
    "ilm.delete_lifecycle": {"policy", "name"},
    "ilm.get_lifecycle": {"policy": "name"},
    "ilm.put_lifecycle": {"policy": "name"},
}

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
    "transform_and_set",
}

# broken YAML tests on some releases
FAILING_TESTS = {
    # ping has a custom implementation in Python and returns a boolean
    "ping/ping",
    # Not investigated yet
    "cat/aliases",
    "cat/fielddata",
    "cluster/delete_voting_config_exclusions",
    "cluster/voting_config_exclusions",
    "entsearch/10_basic",
    "indices/clone",
    "indices/resolve_cluster",
    "indices/settings",
    "indices/split",
    "indices/simulate_template_stack",
    "logstash/10_basic",
    "machine_learning/30_trained_model_stack",
    "machine_learning/jobs_crud",
    "scroll/10_basic",
    "security/10_api_key_basic",
    "transform/10_basic",
}
SKIPPED_TESTS = {
    # Timeouts
    # https://github.com/elastic/elasticsearch-serverless-python/issues/63
    "cluster/cluster_info[0]",
    "inference/10_basic[0]",
    "machine_learning/20_trained_model[0]",
}


XPACK_FEATURES = None
RUN_ASYNC_REST_API_TESTS = os.environ.get("PYTHON_CONNECTION_CLASS") == "requests"

FALSEY_VALUES = ("", None, False, 0, 0.0)


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
        # Pull skips from individual tests to not do unnecessary setup.
        skip_code = []
        for action in self._run_code:
            assert len(action) == 1
            action_type, _ = list(action.items())[0]
            if action_type == "skip":
                skip_code.append(action)
            else:
                break

        if self._setup_code or skip_code:
            self.section("setup")
        if skip_code:
            self.run_code(skip_code)
        if self._setup_code:
            self.run_code(self._setup_code)

    def teardown(self):
        if self._teardown_code:
            self.section("teardown")
            self.run_code(self._teardown_code)

    def section(self, name):
        print(("=" * 10) + " " + name + " " + ("=" * 10))

    def run(self):
        try:
            self.setup()
            self.section("test")
            self.run_code(self._run_code)
        finally:
            try:
                self.teardown()
            except Exception:
                pass

    def run_code(self, test):
        """Execute an instruction based on it's type."""
        for action in test:
            assert len(action) == 1
            action_type, action = list(action.items())[0]
            print(action_type, action)

            if hasattr(self, "run_" + action_type):
                getattr(self, "run_" + action_type)(action)
            else:
                raise RuntimeError(f"Invalid action type {action_type!r}")

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

        if headers:
            args["headers"] = headers

        # locate api endpoint
        for m in method.split("."):
            if not hasattr(api, m):
                pytest.skip("This API isn't implemented yet")
            api = getattr(api, m)

        # Sometimes the 'body' parameter is encoded as a string instead of raw.
        if "body" in args:
            try:
                args["body"] = json.loads(args["body"])
            except (TypeError, ValueError):
                pass

            if isinstance(args["body"], dict):
                # Detect when there are duplicate options that aren't the same value.
                # In this case the test isn't testing the client, it's testing Elasticsearch
                # and its ability to reject multiple values so we either combine
                # like values or skip the test entirely as unnecessary for the client.
                duplicate_args = set(args["body"]).intersection(args)
                if duplicate_args:
                    for arg in list(duplicate_args):
                        if args["body"][arg] == args[arg]:
                            args["body"].pop(arg)
                        else:
                            pytest.skip(
                                "Contains a duplicate parameter with a different value"
                            )

        # some parameters had to be renamed to not clash with python builtins,
        # compensate
        renames = PARAMS_RENAMES.copy()
        renames.update(API_PARAMS_RENAMES.get(method, {}))
        for k in renames:
            if k in args:
                args[renames[k]] = args.pop(k)

        # resolve vars
        for k in args:
            args[k] = self._resolve(args[k])

        warnings.simplefilter("always", category=ElasticsearchWarning)
        with warnings.catch_warnings(record=True) as caught_warnings:
            try:
                self.last_response = api(**args).body
            except Exception as e:
                self._skip_intentional_type_errors(e)
                if not catch:
                    raise
                self.run_catch(catch, e)
            else:
                if catch:
                    raise AssertionError(
                        f"Failed to catch {catch!r} in {self.last_response!r}."
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
        if catch == "param" or isinstance(exception, TypeError):
            assert isinstance(exception, TypeError)
            self.last_response = None
            return

        assert isinstance(exception, ApiError)
        if catch in CATCH_CODES:
            assert CATCH_CODES[catch] == exception.meta.status
        elif catch[0] == "/" and catch[-1] == "/":
            assert (
                re.search(catch[1:-1], str(exception.body)),
                f"{catch} not in {str(exception.body)!r}",
            ) is not None
        self.last_response = exception.body

    def run_skip(self, skip):
        global IMPLEMENTED_FEATURES

        if "features" in skip:
            features = skip["features"]
            if not isinstance(features, (tuple, list)):
                features = [features]
            for feature in features:
                if feature in IMPLEMENTED_FEATURES:
                    continue
                pytest.skip(f"feature '{feature}' is not supported")

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
            assert value in FALSEY_VALUES

    def run_is_true(self, action):
        value = self._lookup(action)
        assert value not in FALSEY_VALUES

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
                assert expected.search(value), f"{value!r} does not match {expected!r}"
            elif isinstance(value, list) and isinstance(expected, list):
                assert len(value) == len(
                    expected
                ), f"Length between {value!r} and {expected!r} wasn't equal"
                [self._assert_match_equals(a, b) for a, b in zip(value, expected)]
            else:
                self._assert_match_equals(value, expected)

    def run_contains(self, action):
        for path, expected in action.items():
            value = self._lookup(path)  # list[dict[str,str]] is returned
            expected = self._resolve(expected)  # dict[str, str]

            if expected not in value:
                raise AssertionError(f"{expected} is not contained by {value}")

    def run_transform_and_set(self, action):
        for key, value in action.items():
            # Convert #base64EncodeCredentials(id,api_key) to ["id", "api_key"]
            if "#base64EncodeCredentials" in value:
                value = value.replace("#base64EncodeCredentials", "")
                value = value.replace("(", "").replace(")", "").split(",")
                self._state[key] = _base64_auth_header(
                    (self._lookup(value[0]), self._lookup(value[1]))
                )

    def _resolve(self, value):
        # resolve variables
        if isinstance(value, string_types) and "$" in value:
            for k, v in self._state.items():
                for key_replace in ("${" + k + "}", "$" + k):
                    if value == key_replace:
                        value = v
                        break
                    # We only do the in-string replacement if using ${...}
                    elif (
                        key_replace.startswith("${")
                        and isinstance(value, string_types)
                        and key_replace in value
                    ):
                        value = value.replace(key_replace, str(v))
                        break
                    # We only do the in-string replacement if value is JSON string
                    # E.g. '{\n  "password_hash" : "$hash"\n}\n'
                    elif (
                        key_replace.startswith("$")
                        and isinstance(value, string_types)
                        and key_replace in value
                        and not value.startswith("$")
                    ):
                        value = value.replace(key_replace, str(v))
                        break

        if isinstance(value, string_types):
            value = value.strip()
        elif isinstance(value, dict):
            value = {k: self._resolve(v) for (k, v) in value.items()}
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
            # We check body again to handle E.g. '$body.$backing_index.data_stream'
            if step.startswith("$body"):
                continue
            step = step.replace("\1", ".")
            step = self._resolve(step)
            if (
                isinstance(step, string_types)
                and step.isdigit()
                and isinstance(value, list)
            ):
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
                XPACK_FEATURES = {
                    f for f in xinfo["features"] if xinfo["features"][f]["enabled"]
                }
                IMPLEMENTED_FEATURES.add("xpack")
            except RequestError:
                XPACK_FEATURES = set()
                IMPLEMENTED_FEATURES.add("no_xpack")
        return name in XPACK_FEATURES

    def _assert_match_equals(self, a, b):
        # Handle for large floating points with 'E'
        if isinstance(b, string_types) and isinstance(a, float) and "e" in repr(a):
            a = repr(a).replace("e+", "E")

        assert a == b, f"{a!r} does not match {b!r}"

    def _skip_intentional_type_errors(self, e: Exception):
        if isinstance(e, TypeError) and (
            "unexpected keyword argument" in str(e)
            or "required keyword-only argument" in str(e)
        ):
            pytest.skip("API intentionally used incorrectly in test")


@pytest.fixture(scope="function")
def sync_runner(sync_client_factory):
    # sync_client_factory does not wipe the cluster between tests
    return YamlRunner(sync_client_factory)


# Source: https://stackoverflow.com/a/37958106/5763213
class NoDatesSafeLoader(yaml.SafeLoader):
    @classmethod
    def remove_implicit_resolver(cls, tag_to_remove):
        # Make a copy from the parent class to ensure
        # we're not modifying the parent.
        if "yaml_implicit_resolvers" not in cls.__dict__:
            cls.yaml_implicit_resolvers = cls.yaml_implicit_resolvers.copy()

        # Remove the resolver everywhere it shows up.
        for key, mappings in cls.yaml_implicit_resolvers.items():
            cls.yaml_implicit_resolvers[key] = [
                (tag, regexp) for tag, regexp in mappings if tag != tag_to_remove
            ]


# We don't want to magically load date/times into objects. Keep as strings.
NoDatesSafeLoader.remove_implicit_resolver("tag:yaml.org,2002:timestamp")


YAML_TEST_SPECS = []

# Try loading the REST API test specs from the Elastic Artifacts API
try:
    # Construct the HTTP and Elasticsearch client
    http = urllib3.PoolManager(retries=10)

    yaml_tests_url = (
        "https://api.github.com/repos/elastic/elasticsearch-clients-tests/zipball/main"
    )

    # Download the zip and start reading YAML from the files in memory
    package_zip = zipfile.ZipFile(io.BytesIO(http.request("GET", yaml_tests_url).data))

    for yaml_file in package_zip.namelist():
        if not re.match(r"^.*\/tests\/.*\.ya?ml$", yaml_file):
            continue
        yaml_tests = list(
            yaml.load_all(package_zip.read(yaml_file), Loader=NoDatesSafeLoader)
        )

        # Each file has a `requires` section with `serverless` and `stack`
        # boolean entries indicating whether the test should run with
        # serverless, stack or both. Additionally, each file may have a section
        # named 'setup' or 'teardown', these sets of steps should be run at the
        # beginning and end of every other test within the file so we do one
        # pass to capture those.
        requires = setup_steps = teardown_steps = None
        test_numbers_and_steps = []
        test_number = 0

        for yaml_test in yaml_tests:
            test_name, test_step = yaml_test.popitem()
            if test_name == "requires":
                requires = test_step
            elif test_name == "setup":
                setup_steps = test_step
            elif test_name == "teardown":
                teardown_steps = test_step
            else:
                test_numbers_and_steps.append((test_number, test_step))
                test_number += 1

        if not requires["stack"]:
            continue

        # Now we combine setup, teardown, and test_steps into
        # a set of pytest.param() instances
        for test_number, test_step in test_numbers_and_steps:
            # Build the id from the name of the YAML file and the number within
            # that file. Most important step is to remove most of the file path
            # prefixes and the .yml suffix.
            test_path = "/".join(yaml_file.split("/")[2:])
            pytest_test_name = test_path.rpartition(".")[0].replace(".", "/")
            for prefix in ("rest-api-spec/", "test/", "free/", "platinum/"):
                if pytest_test_name.startswith(prefix):
                    pytest_test_name = pytest_test_name[len(prefix) :]
            pytest_param_id = "%s[%d]" % (pytest_test_name, test_number)

            pytest_param = {
                "setup": setup_steps,
                "run": test_step,
                "teardown": teardown_steps,
            }
            # Skip either 'test_name' or 'test_name[x]'
            if pytest_test_name in FAILING_TESTS or pytest_param_id in FAILING_TESTS:
                pytest_param["fail"] = True
            elif pytest_test_name in SKIPPED_TESTS or pytest_param_id in SKIPPED_TESTS:
                pytest_param["skip"] = True

            YAML_TEST_SPECS.append(pytest.param(pytest_param, id=pytest_param_id))

except Exception as e:
    warnings.warn(f"Could not load REST API tests: {str(e)}")


def _pytest_param_sort_key(param: pytest.param) -> Tuple[Union[str, int], ...]:
    # Sorts pytest parameters by their ID in a human-friendly way.
    return tuple(int(x) if x.isdigit() else x for x in re.split(r"([0-9]+)", param.id))


# Sort the tests by ID so they're grouped together nicely.
YAML_TEST_SPECS = sorted(YAML_TEST_SPECS, key=_pytest_param_sort_key)

if not RUN_ASYNC_REST_API_TESTS:

    @pytest.mark.parametrize("test_spec", YAML_TEST_SPECS)
    def test_rest_api_spec(test_spec, sync_runner):
        if test_spec.get("fail", False):
            pytest.xfail("Manually marked as failing in 'FAILING_TESTS'")
        elif test_spec.get("skip", False):
            pytest.skip("Manually marked as skipped")
        sync_runner.use_spec(test_spec)
        sync_runner.run()
