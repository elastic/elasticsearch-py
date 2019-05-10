# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import ElasticsearchTestCase


class TestUnicode(ElasticsearchTestCase):
    def test_indices_analyze(self):
        self.client.indices.analyze(body='{"text": "привет"}')
