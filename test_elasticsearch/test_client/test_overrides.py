# -*- coding: utf-8 -*-
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

import pytest

from .common import DummyTransportTestCase


class TestOverriddenUrlTargets(DummyTransportTestCase):
    @pytest.mark.parametrize(
        ["doc_type", "url_suffix"],
        [(None, "/_create/test-id"), ("test-type", "/test-type/test-id/_create")],
    )
    def test_create(self, doc_type, url_suffix):
        self.client.create(index="test-index", doc_type=doc_type, id="test-id", body={})
        self.assert_helper("PUT", "/test-index" + url_suffix)

    @pytest.mark.parametrize(
        ["doc_type", "url_suffix"],
        [(None, "/_doc/test-id"), ("test-type", "/test-type/test-id")],
    )
    def test_delete(self, doc_type, url_suffix):
        self.client.delete(index="test-index", doc_type=doc_type, id="test-id")
        self.assert_helper("DELETE", "/test-index" + url_suffix)

    @pytest.mark.parametrize(
        ["doc_type", "url_suffix"],
        [(None, "/_update/test-id"), ("test-type", "/test-type/test-id/_update")],
    )
    def test_update(self, doc_type, url_suffix):
        self.client.update(index="test-index", doc_type=doc_type, id="test-id", body={})
        self.assert_helper("POST", "/test-index" + url_suffix)

    @pytest.mark.parametrize(
        ["request_method", "id", "url_suffix"],
        [("POST", None, ""), ("PUT", "test-id", "/test-id")],
    )
    def test_index(self, request_method, id, url_suffix):
        self.client.index(index="test-index", id=id, body={})
        self.assert_helper(request_method, "/test-index/_doc" + url_suffix)
