# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from ..exceptions import ElasticsearchException


class BulkIndexError(ElasticsearchException):
    @property
    def errors(self):
        """ List of errors from execution of the last chunk. """
        return self.args[1]


class ScanError(ElasticsearchException):
    def __init__(self, scroll_id, *args, **kwargs):
        super(ScanError, self).__init__(*args, **kwargs)
        self.scroll_id = scroll_id
