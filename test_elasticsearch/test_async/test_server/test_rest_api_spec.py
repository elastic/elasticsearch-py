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
Dynamically generated set of TestCases based on set of yaml files decribing
some integration tests. These files are shared among all official Elasticsearch
clients.
"""
import inspect
import re
import warnings

import pytest

from elasticsearch import ElasticsearchWarning, RequestError
from elasticsearch.helpers.test import _get_version

from ...test_server.test_rest_api_spec import (
    APIS_USING_TYPE_INSTEAD_OF_DOC_TYPE,
    APIS_WITH_BODY_FIELDS,
    COMPATIBILITY_MIMETYPE,
    COMPATIBILITY_MODE_ENABLED,
    IMPLEMENTED_FEATURES,
    PARAMS_RENAMES,
    RUN_ASYNC_REST_API_TESTS,
    YAML_TEST_SPECS,
    YamlRunner,
)

pytestmark = pytest.mark.asyncio

XPACK_FEATURES = None
ES_VERSION = None


async def await_if_coro(x):
    if inspect.iscoroutine(x):
        return await x
    return x


class AsyncYamlRunner(YamlRunner):
    async def setup(self):
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
            await self.run_code(skip_code)
        if self._setup_code:
            await self.run_code(self._setup_code)

    async def teardown(self):
        if self._teardown_code:
            self.section("teardown")
            await self.run_code(self._teardown_code)

    async def es_version(self):
        global ES_VERSION
        if ES_VERSION is None:
            version_string = (await self.client.info())["version"]["number"]
            if "." not in version_string:
                return ()
            version = version_string.strip().split(".")
            ES_VERSION = tuple(int(v) if v.isdigit() else 999 for v in version)
        return ES_VERSION

    def section(self, name):
        print(("=" * 10) + " " + name + " " + ("=" * 10))

    async def run(self):
        try:
            await self.setup()
            self.section("test")
            await self.run_code(self._run_code)
        finally:
            try:
                await self.teardown()
            except Exception:
                pass

    async def run_code(self, test):
        """Execute an instruction based on it's type."""
        for action in test:
            assert len(action) == 1
            action_type, action = list(action.items())[0]
            print(action_type, action)

            if hasattr(self, "run_" + action_type):
                await await_if_coro(getattr(self, "run_" + action_type)(action))
            else:
                raise RuntimeError("Invalid action type %r" % (action_type,))

    async def run_do(self, action):
        api = self.client
        headers = action.pop("headers", None)
        catch = action.pop("catch", None)
        warn = action.pop("warnings", ())
        allowed_warnings = action.pop("allowed_warnings", ())
        if isinstance(allowed_warnings, str):
            allowed_warnings = (allowed_warnings,)
        allowed_warnings_regex = action.pop("allowed_warnings_regex", ())
        if isinstance(allowed_warnings_regex, str):
            allowed_warnings_regex = (allowed_warnings_regex,)
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

        if headers and "Content-Type" in headers and COMPATIBILITY_MODE_ENABLED:
            headers["Content-Type"] = COMPATIBILITY_MIMETYPE

        method, args = list(action.items())[0]
        args["headers"] = headers

        # locate api endpoint
        for m in method.split("."):
            # Some deprecated APIs are prefixed with 'xpack-*'
            if m.startswith("xpack-"):
                m = m.replace("xpack-", "")
            assert hasattr(api, m)
            api = getattr(api, m)

        # some parameters had to be renamed to not clash with python builtins,
        # compensate
        for k in PARAMS_RENAMES:

            # Don't do the 'doc_type' rename for APIs that actually want 'type'
            if k == "type" and method in APIS_USING_TYPE_INSTEAD_OF_DOC_TYPE:
                continue

            if k in args:
                args[PARAMS_RENAMES[k]] = args.pop(k)

        # resolve vars
        for k in args:
            args[k] = self._resolve(args[k])

        # If there's a body parameter given to an API with
        # body fields enabled we expand the body to parameters.
        if (
            "body" in args
            and isinstance(args["body"], dict)
            and method in APIS_WITH_BODY_FIELDS
        ):
            args.update(
                {PARAMS_RENAMES.get(k, k): v for k, v in args.pop("body").items()}
            )

        warnings.simplefilter("always", category=ElasticsearchWarning)
        with warnings.catch_warnings(record=True) as caught_warnings:
            try:
                self.last_response = await api(**args)
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
            and (not allowed_warnings or str(w.message) not in allowed_warnings)
            and (
                not allowed_warnings_regex
                or all(
                    re.search(pattern, str(w.message)) is None
                    for pattern in allowed_warnings_regex
                )
            )
        ]

        # This warning can show up in many places but isn't accounted for
        # in tests, so we remove it to make sure things pass.
        include_type_name_warning = (
            "[types removal] Using include_type_name in create index requests is deprecated. "
            "The parameter will be removed in the next major version."
        )
        if (
            include_type_name_warning in caught_warnings
            and include_type_name_warning not in warn
        ):
            caught_warnings.remove(include_type_name_warning)

        # Sorting removes the issue with order raised. We only care about
        # if all warnings are raised in the single API call.
        if warn and sorted(warn) != sorted(caught_warnings):
            raise AssertionError(
                "Expected warnings not equal to actual warnings: expected=%r actual=%r"
                % (warn, caught_warnings)
            )

    async def run_skip(self, skip):
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
            if min_version <= (await self.es_version()) <= max_version:
                pytest.skip(reason)

    async def _feature_enabled(self, name):
        global XPACK_FEATURES
        if XPACK_FEATURES is None:
            try:
                xinfo = await self.client.xpack.info()
                XPACK_FEATURES = set(
                    f for f in xinfo["features"] if xinfo["features"][f]["enabled"]
                )
                IMPLEMENTED_FEATURES.add("xpack")
            except RequestError:
                XPACK_FEATURES = set()
                IMPLEMENTED_FEATURES.add("no_xpack")
        return name in XPACK_FEATURES


@pytest.fixture(scope="function")
def async_runner(async_client):
    return AsyncYamlRunner(async_client)


if RUN_ASYNC_REST_API_TESTS:

    @pytest.mark.parametrize("test_spec", YAML_TEST_SPECS)
    async def test_rest_api_spec(test_spec, async_runner):
        if test_spec.get("skip", False):
            pytest.skip("Manually skipped in 'SKIP_TESTS'")
        async_runner.use_spec(test_spec)
        await async_runner.run()
