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

import importlib
import sys
import warnings

import pytest

import elasticsearch


@pytest.mark.skipif(sys.version_info < (3, 6), reason="Requires Python 3.6+")
def test_no_deprecation_python3_6_and_later():
    with warnings.catch_warnings(record=True) as w:
        importlib.reload(elasticsearch)

    assert len(w) == 0


@pytest.mark.skipif(sys.version_info >= (3, 6), reason="Requires Python <3.6")
def test_deprecated_python3_5_and_earlier():

    try:  # Python 3.4+
        import imp

        reload = imp.reload
    except ImportError:  # Python 2.7
        reload = reload

    with pytest.warns(DeprecationWarning) as w:
        reload(elasticsearch)

    assert len(w) == 1
    assert str(w[0].message) == (
        "Support for Python 3.5 and earlier is deprecated and will be removed "
        "in v8.0.0 (current instance is Python %d.%d) See https://github.com/"
        "elastic/elasticsearch-py/issues/1696 for details." % (sys.version_info[:2])
    )
