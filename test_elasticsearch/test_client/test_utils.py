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

from __future__ import unicode_literals

from elasticsearch._sync.client.utils import _quote


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
