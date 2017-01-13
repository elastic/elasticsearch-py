#!/usr/bin/env python
from __future__ import print_function

import logging
from dateutil.parser import parse as parse_date

from elasticsearch5 import Elasticsearch

def print_search_stats(results):
    print('=' * 80)
    print('Total %d found in %dms' % (results['hits']['total'], results['took']))
    print('-' * 80)

def print_hits(results):
    " Simple utility function to print results of a search query. "
    print_search_stats(results)
    for hit in results['hits']['hits']:
        # get created date for a repo and fallback to authored_date for a commit
        created_at = parse_date(hit['_source'].get('created_at', hit['_source']['authored_date']))
        print('/%s/%s/%s (%s): %s' % (
                hit['_index'], hit['_type'], hit['_id'],
                created_at.strftime('%Y-%m-%d'),
                hit['_source']['description'].replace('\n', ' ')))

    print('=' * 80)
    print()

# get trace logger and set level
tracer = logging.getLogger('from elasticsearch5.trace')
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
        'bool': {
          'must': {
            'match': {'description': 'fix'}
          },
          'must_not': {
            'term': {'files': 'test_elasticsearch'}
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
        'parent_id': {
            'type': 'commits', 'id': 'elasticsearch-py'
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
        'has_parent': {
          'parent_type': 'repos',
          'query': {
            'term': {
              'tags': 'python'
            }
          }
        }
      },
      'aggs': {
        'committers': {
          'terms': {
            'field': 'committer.name.raw',
          },
          'aggs': {
            'line_stats': {
              'stats': {'field': 'stats.lines'}
            }
          }
        }
      }
    }
)

print_search_stats(result)
for committer in result['aggregations']['committers']['buckets']:
    print('%15s: %3d commits changing %6d lines' % (
        committer['key'], committer['doc_count'], committer['line_stats']['sum']))
print('=' * 80)
