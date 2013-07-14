# -*- coding: utf-8 -*-
from unittest import TestCase, SkipTest

from elasticsearch.client.utils import _make_path

class TestMakePath(TestCase):
    def test_handles_unicode(self):
        id = u"中文"
        self.assertEquals('/some-index/type/%E4%B8%AD%E6%96%87', _make_path('some-index', 'type', id))

    def test_handles_utf_encoded_string(self):
        if type('') is type(u''):
            raise SkipTest('Only relevant for py2')
        id = u"中文".encode('utf-8')
        self.assertEquals('/some-index/type/%E4%B8%AD%E6%96%87', _make_path('some-index', 'type', id))

