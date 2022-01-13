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

from elastic_transport import ApiResponseMeta

from elasticsearch.exceptions import ApiError

error_meta = ApiResponseMeta(
    status=500, http_version="1.1", headers={}, duration=0.0, node=None
)


class TestTransformError:
    def test_transform_error_parse_with_error_reason(self):
        e = ApiError(
            message="InternalServerError",
            meta=error_meta,
            body={
                "error": {"root_cause": [{"type": "error", "reason": "error reason"}]}
            },
        )

        assert str(e) == "ApiError(500, 'InternalServerError', 'error reason')"

    def test_transform_error_parse_with_error_string(self):
        e = ApiError(
            message="InternalServerError",
            meta=error_meta,
            body={"error": "something error message"},
        )

        assert (
            str(e) == "ApiError(500, 'InternalServerError', 'something error message')"
        )
