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

    def test_transform_invalid_media_type_error(self):
        e = ApiError(
            message="InvalidMediaType",
            meta=error_meta,
            body={
                "error": {
                    "root_cause": [
                        {
                            "type": "media_type_header_exception",
                            "reason": "Invalid media-type value on headers [Accept, Content-Type]",
                        }
                    ],
                    "type": "media_type_header_exception",
                    "reason": "Invalid media-type value on headers [Accept, Content-Type]",
                    "caused_by": {
                        "type": "status_exception",
                        "reason": "Accept version must be either version 8 or 7, but found 9. Accept=application/vnd.elasticsearch+json; compatible-with=9",
                    },
                },
                "status": 400,
            },
        )

        assert str(e) == (
            "ApiError(500, 'InvalidMediaType', "
            "'Invalid media-type value on headers [Accept, Content-Type]', "
            "Accept version must be either version 8 or 7, but found 9. "
            "Accept=application/vnd.elasticsearch+json; compatible-with=9)"
        )

    def test_transform_error_with_list_resource_id(self):
        e = ApiError(
            message="NotFoundError",
            meta=error_meta,
            body={
                "error": {
                    "root_cause": [
                        {
                            "type": "index_not_found_exception",
                            "reason": "no such index [test-1, test-2]",
                            "resource.type": "index_or_alias",
                            "resource.id": ["test-1", "test-2"],
                        }
                    ]
                }
            },
        )
        assert (
            str(e)
            == "ApiError(500, 'NotFoundError', 'no such index [test-1, test-2]', test-1, test-2, index_or_alias)"
        )

    def test_transform_error_with_non_string_resource_fields(self):
        e = ApiError(
            message="NotFoundError",
            meta=error_meta,
            body={
                "error": {
                    "root_cause": [
                        {
                            "type": "error",
                            "reason": "missing",
                            "resource.id": 12345,
                            "resource.type": ["type1", "type2"],
                        }
                    ],
                    "caused_by": {"reason": 999},
                }
            },
        )
        assert (
            str(e)
            == "ApiError(500, 'NotFoundError', 'missing', 12345, type1, type2, 999)"
        )

    def test_transform_error_with_non_dict_caused_by(self):
        e = ApiError(
            message="InternalServerError",
            meta=error_meta,
            body={
                "error": {
                    "root_cause": [{"type": "error", "reason": "failure"}],
                    "caused_by": "not a dict",
                }
            },
        )
        assert str(e) == "ApiError(500, 'InternalServerError', 'failure')"
