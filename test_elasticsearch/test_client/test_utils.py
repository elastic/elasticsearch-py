# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from elasticsearch.client.utils import _make_path
from elasticsearch.compat import PY2

from ..test_cases import TestCase, SkipTest

class TestMakePath(TestCase):
    def test_handles_unicode(self):
        id = "中文"
        self.assertEquals('/some-index/type/%E4%B8%AD%E6%96%87', _make_path('some-index', 'type', id))

    def test_handles_utf_encoded_string(self):
        if not PY2:
            raise SkipTest('Only relevant for py2')
        id = "中文".encode('utf-8')
        self.assertEquals('/some-index/type/%E4%B8%AD%E6%96%87', _make_path('some-index', 'type', id))

