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


def test_text_response(sync_client):
    resp = sync_client.cat.tasks()
    assert resp.meta.status == 200
    assert isinstance(resp.raw, str)
    assert str(resp.raw) == str(resp)


def test_object_response(sync_client):
    resp = sync_client.search(size=1)
    assert isinstance(resp.raw, dict)
    assert set(resp) == set(resp.raw)
    assert resp.items()
    assert resp.keys()
    assert str(resp) == str(resp.raw)
    assert resp["hits"] == resp.raw["hits"]
    assert type(resp.copy()) is dict


def test_exists_response(sync_client):
    resp = sync_client.indices.exists(index="no")
    assert resp.raw is False
    assert not resp
    if resp:
        assert False, "Didn't evaluate to 'False'"
    assert str(resp) == "False"
