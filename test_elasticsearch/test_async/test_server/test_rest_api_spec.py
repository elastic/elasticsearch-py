# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

"""
Dynamically generated set of TestCases based on set of yaml files decribing
some integration tests. These files are shared among all official Elasticsearch
clients.
"""
import pytest
from shutil import rmtree
import warnings
import inspect

from elasticsearch import RequestError, ElasticsearchDeprecationWarning
from elasticsearch.helpers.test import _get_version
from ...test_server.test_rest_api_spec import (
    YamlRunner,
    YAML_TEST_SPECS,
    InvalidActionType,
    RUN_ASYNC_REST_API_TESTS,
    PARAMS_RENAMES,
    IMPLEMENTED_FEATURES,
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
        if self._setup_code:
            await self.run_code(self._setup_code)

    async def teardown(self):
        if self._teardown_code:
            await self.run_code(self._teardown_code)

        for repo, definition in (
            await self.client.snapshot.get_repository(repository="_all")
        ).items():
            await self.client.snapshot.delete_repository(repository=repo)
            if definition["type"] == "fs":
                rmtree(
                    "/tmp/%s" % definition["settings"]["location"], ignore_errors=True
                )

        # stop and remove all ML stuff
        if await self._feature_enabled("ml"):
            await self.client.ml.stop_datafeed(datafeed_id="*", force=True)
            for feed in (await self.client.ml.get_datafeeds(datafeed_id="*"))[
                "datafeeds"
            ]:
                await self.client.ml.delete_datafeed(datafeed_id=feed["datafeed_id"])

            await self.client.ml.close_job(job_id="*", force=True)
            for job in (await self.client.ml.get_jobs(job_id="*"))["jobs"]:
                await self.client.ml.delete_job(
                    job_id=job["job_id"], wait_for_completion=True, force=True
                )

        # stop and remove all Rollup jobs
        if await self._feature_enabled("rollup"):
            for rollup in (await self.client.rollup.get_jobs(id="*"))["jobs"]:
                await self.client.rollup.stop_job(
                    id=rollup["config"]["id"], wait_for_completion=True
                )
                await self.client.rollup.delete_job(id=rollup["config"]["id"])

    async def es_version(self):
        global ES_VERSION
        if ES_VERSION is None:
            version_string = (await self.client.info())["version"]["number"]
            if "." not in version_string:
                return ()
            version = version_string.strip().split(".")
            ES_VERSION = tuple(int(v) if v.isdigit() else 999 for v in version)
        return ES_VERSION

    async def run(self):
        try:
            await self.setup()
            await self.run_code(self._run_code)
        finally:
            await self.teardown()

    async def run_code(self, test):
        """ Execute an instruction based on it's type. """
        print(test)
        for action in test:
            assert len(action) == 1
            action_type, action = list(action.items())[0]

            if hasattr(self, "run_" + action_type):
                await await_if_coro(getattr(self, "run_" + action_type)(action))
            else:
                raise InvalidActionType(action_type)

    async def run_do(self, action):
        api = self.client
        headers = action.pop("headers", None)
        catch = action.pop("catch", None)
        warn = action.pop("warnings", ())
        allowed_warnings = action.pop("allowed_warnings", ())
        assert len(action) == 1

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

        warnings.simplefilter("always", category=ElasticsearchDeprecationWarning)
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
            if w.category == ElasticsearchDeprecationWarning
            and str(w.message) not in allowed_warnings
        ]

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


@pytest.mark.parametrize("test_spec", YAML_TEST_SPECS)
async def test_rest_api_spec(test_spec, async_runner):
    if not RUN_ASYNC_REST_API_TESTS:
        pytest.skip("Skipped running async REST API tests")
    if test_spec.get("skip", False):
        pytest.skip("Manually skipped in 'SKIP_TESTS'")
    async_runner.use_spec(test_spec)
    await async_runner.run()
