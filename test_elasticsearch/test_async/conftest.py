# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

import sys
import pytest

pytestmark = pytest.mark.skipif(
    sys.version_info < (3, 6), reason="'test_async' is only run on Python 3.6+"
)
