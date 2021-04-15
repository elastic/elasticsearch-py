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

import binascii
import re


def _client_meta_version(version):
    """Transforms a Python package version to one
    compatible with 'X-Elastic-Client-Meta'. Essentially
    replaces any pre-release information with a 'p' suffix.
    """
    version, version_pre = re.match(
        r"^([0-9][0-9.]*[0-9]|[0-9])(.*)$", version
    ).groups()
    if version_pre:
        version += "p"
    return version


def get_api_key_header_val(api_key):
    """
    Check the type of the passed api_key and return the correct header value
    for the `API Key authentication <https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html>`
    :arg api_key, either a tuple or a base64 encoded string
    """
    if isinstance(api_key, (tuple, list)):
        s = "{0}:{1}".format(api_key[0], api_key[1]).encode("utf-8")
        return "ApiKey " + binascii.b2a_base64(s).rstrip(b"\r\n").decode("utf-8")
    return "ApiKey " + api_key
