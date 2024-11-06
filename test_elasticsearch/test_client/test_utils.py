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


import warnings

from elasticsearch._sync.client.utils import Stability, _quote, _stability_warning
from elasticsearch.exceptions import GeneralAvailabilityWarning


def test_handles_ascii():
    string = "abc123"
    assert "abc123" == _quote(string)


def test_handles_bytestring():
    string = b"celery-task-meta-c4f1201f-eb7b-41d5-9318-a75a8cfbdaa0"
    assert string.decode() == _quote(string)


def test_handles_unicode():
    assert "some-index-type-%E4%B8%AD%E6%96%87" == _quote("some-index-type-中文")


def test_handles_unicode2():
    string = "中*文,"
    assert "%E4%B8%AD*%E6%96%87," == _quote(string)


class TestStabilityWarning:
    def test_default(self):

        @_stability_warning(stability=Stability.STABLE)
        def func_default(*args, **kwargs):
            pass

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            func_default()

    def test_beta(self, recwarn):

        @_stability_warning(stability=Stability.BETA)
        def func_beta(*args, **kwargs):
            pass

        func_beta()

        assert len(recwarn) == 1
        user_warning = recwarn.pop(GeneralAvailabilityWarning)
        assert user_warning.category == GeneralAvailabilityWarning
        assert user_warning.message.args[0].startswith(
            "This API is in beta and is subject to change."
        )

    def test_experimental(self, recwarn):

        @_stability_warning(stability=Stability.EXPERIMENTAL)
        def func_experimental(*args, **kwargs):
            pass

        func_experimental()

        assert len(recwarn) == 1
        user_warning = recwarn.pop(GeneralAvailabilityWarning)
        assert user_warning.category == GeneralAvailabilityWarning
        assert user_warning.message.args[0].startswith(
            "This API is in technical preview and may be changed or removed in a future release."
        )

    def test_deprecated(self, recwarn):

        @_stability_warning(
            stability=Stability.DEPRECATED, version="8.4.0", message="Use bar instead."
        )
        def func_deprecated(*args, **kwargs):
            pass

        func_deprecated()

        assert len(recwarn) == 1
        user_warning = recwarn.pop(DeprecationWarning)
        assert user_warning.category == DeprecationWarning
        assert user_warning.message.args[0] == (
            "This API was deprecated in Elasticsearch 8.4.0. Use bar instead."
        )
