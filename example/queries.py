#!/usr/bin/env python
from __future__ import print_function

import logging
from dateutil.parser import parse as parse_date

from elasticsearch import Elasticsearch

def print_hits(results, facet_masks={}):
    " Simple utility function to print results of a search query. "
    print('=' * 80)
    print('Total %d found in %dms' % (results['hits']['total'], results['took']))
    if results['hits']['hits']:
        print('-' * 80)
    for hit in results['hits']['hits']:
        # get created date for a repo and fallback to authored_date for a commit
        created_at = parse_date(hit['_source'].get('created_at', hit['_source']['authored_date']))
        print('/%s/%s/%s (%s): %s' % (
                hit['_index'], hit['_type'], hit['_id'],
                created_at.strftime('%Y-%m-%d'),
                hit['_source']['description'].replace('\n', ' ')))

    for facet, mask in facet_masks.items():
        print('-' * 80)
        for d in results['facets'][facet]['terms']:
            print(mask % d)
    print('=' * 80)
    print()

# get trace logger and set level
tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
tracer.addHandler(logging.FileHandler('/tmp/es_trace.log'))
# instantiate es client, connects to localhost:9200 by default
es = Elasticsearch()

print('Empty search:')
print_hits(es.search(index='git'))

print('Find commits that says "fix" without touching tests:')
result = es.search(
    index='git',
    doc_type='commits',
    body={
      'query': {
        'filtered': {
          'query': {
            'match': {'description': 'fix'}
          },
          'filter': {
            'not': {
              'term': {'files': 'test_elasticsearch'}
            }
          }
        }
      }
    }
)
print_hits(result)

print('Last 8 Commits for elasticsearch-py:')
result = es.search(
    index='git',
    doc_type='commits',
    body={
      'query': {
        'filtered': {
          'filter': {
            'term': {
              # parent ref is stored as type#id
              '_parent': 'repos#elasticsearch-py'
            }
          }
        }
      },
      'sort': [
        {'committed_date': {'order': 'desc'}}
      ],
      'size': 8
    }
)
print_hits(result)

print('Stats for top 10 python committers:')
result = es.search(
    index='git',
    doc_type='commits',
    body={
      'size': 0,
      'query': {
        'filtered': {
          'filter': {
            'has_parent': {
              'type': 'repos',
              'query': {
                'filtered': {
                  'filter': {
                    'term': {
                      'tags': 'python'
                    }
                  }
                }
              }
            }
          }
        }
      },
      'facets': {
        'committers': {
          'terms_stats': {
            'key_field': 'committer.name.raw',
            'value_field': 'stats.lines'
          }
        }
      }
    }
)
print_hits(result, {'committers': '%(term)15s: %(count)3d commits changing %(total)6d lines'})

