# -*- coding:utf8 -*-
import unittest
import random
import time

from elasticsearch import Elasticsearch

ES_CONF = {
    'index': 'es_index_test',
    'doc_type': 'pixel',
    'hosts': 'https://localhost:9200'
}


class TestElasticsearchFieldsLimit(unittest.TestCase):
    '''
    trigger TransportError use ES version 5.x.
    '''

    def __doc(self, es):
        dsl = {'size': 10000, '_source': [], 'query': {'constant_score': {'filter': {'bool': {'must': [{'term': {'ds': '2017-01-01'}}, {'term': {'unit_name': 'ds__product_id'}}]}}}}}
        return es.search(index=ES_CONF['index'], doc_type=ES_CONF['doc_type'], body=dsl)

    def test_trigger_TransportError(self):
        es = Elasticsearch(ES_CONF['hosts'])

        update_doc = {"ds": "2018-01-01", "product_id": "21", 'five_minutes_online_ips_distribution': {'190': 0}, "unit_name": "ds__product_id"}
        docs = self.__doc(es)
        if docs['hits']['total'] == 0:
            r = es.index(index=ES_CONF['index'], doc_type=ES_CONF['doc_type'], body=update_doc)
            time.sleep(2)

        docs = self.__doc(es)
        self.assertEquals(1, len(docs['hits']['hits']))
        doc_id = docs['hits']['hits'][0]['_id']

        for i in range(1110):
            update_doc['five_minutes_online_ips_distribution'] = {i: random.randint(1, 100)}
            try:
                r = es.update(index=ES_CONF['index'], doc_type=ES_CONF['doc_type'], id=doc_id, body={'doc': update_doc})
            except Exception as e:
                self.assertRegexpMatches(str(e), 'Limit of total fields ')
                break


if __name__ == "__main__":
    unittest.main()
