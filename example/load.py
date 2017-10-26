#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from os.path import dirname, basename, abspath
from datetime import datetime
import logging
import sys
import argparse

import git

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

def create_git_index(client, index):
    # we will use user on several places
    user_mapping = {
      'properties': {
        'name': {
          'type': 'text',
          'fields': {
            'raw': {'type': 'keyword'},
          }
        }
      }
    }

    create_index_body = {
      'settings': {
        # just one shard, no replicas for testing
        'number_of_shards': 1,
        'number_of_replicas': 0,

        # custom analyzer for analyzing file paths
        'analysis': {
          'analyzer': {
            'file_path': {
              'type': 'custom',
              'tokenizer': 'path_hierarchy',
              'filter': ['lowercase']
            }
          }
        }
      },
      'mappings': {
        'commits': {
          '_parent': {
            'type': 'repos'
          },
          'properties': {
            'repository': {'type': 'keyword'},
            'author': user_mapping,
            'authored_date': {'type': 'date'},
            'committer': user_mapping,
            'committed_date': {'type': 'date'},
            'parent_shas': {'type': 'keyword'},
            'description': {'type': 'text', 'analyzer': 'snowball'},
            'files': {'type': 'text', 'analyzer': 'file_path', "fielddata": True}
          }
        },
        'repos': {
          'properties': {
            'owner': user_mapping,
            'created_at': {'type': 'date'},
            'description': {
              'type': 'text',
              'analyzer': 'snowball',
            },
            'tags': {'type': 'keyword'}
          }
        }
      }
    }

    # create empty index
    try:
        client.indices.create(
            index=index,
            body=create_index_body,
        )
    except TransportError as e:
        # ignore already existing index
        if e.error == 'index_already_exists_exception':
            pass
        else:
            raise

def parse_commits(head, name):
    """
    Go through the git repository log and generate a document per commit
    containing all the metadata.
    """
    for commit in head.traverse():
        yield {
            '_id': commit.hexsha,
            '_parent': name,
            'repository': name,
            'committed_date': datetime.fromtimestamp(commit.committed_date),
            'committer': {
                'name': commit.committer.name,
                'email': commit.committer.email,
            },
            'authored_date': datetime.fromtimestamp(commit.authored_date),
            'author': {
                'name': commit.author.name,
                'email': commit.author.email,
            },
            'description': commit.message,
            'parent_shas': [p.hexsha for p in commit.parents],
            # we only care about the filenames, not the per-file stats
            'files': list(commit.stats.files),
            'stats': commit.stats.total,
        }

def load_repo(client, path=None, index='git'):
    """
    Parse a git repository with all it's commits and load it into elasticsearch
    using `client`. If the index doesn't exist it will be created.
    """
    path = dirname(dirname(abspath(__file__))) if path is None else path
    repo_name = basename(path)
    repo = git.Repo(path)

    create_git_index(client, index)

    # create the parent document in case it doesn't exist
    client.create(
        index=index,
        doc_type='repos',
        id=repo_name,
        body={},
        ignore=409 # 409 - conflict - would be returned if the document is already there
    )

    # we let the streaming bulk continuously process the commits as they come
    # in - since the `parse_commits` function is a generator this will avoid
    # loading all the commits into memory
    for ok, result in streaming_bulk(
            client,
            parse_commits(repo.refs.master.commit, repo_name),
            index=index,
            doc_type='commits',
            chunk_size=50 # keep the batch sizes small for appearances only
        ):
        action, result = result.popitem()
        doc_id = '/%s/commits/%s' % (index, result['_id'])
        # process the information from ES whether the document has been
        # successfully indexed
        if not ok:
            print('Failed to %s document %s: %r' % (action, doc_id, result))
        else:
            print(doc_id)


# we manually create es repo document and update elasticsearch-py to include metadata
REPO_ACTIONS = [
    {'_type': 'repos', '_id': 'elasticsearch', '_source': {
        'owner': {'name': 'Shay Bannon', 'email': 'kimchy@gmail.com'},
        'created_at': datetime(2010, 2, 8, 15, 22, 27),
        'tags': ['search', 'distributed', 'lucene'],
        'description': 'You know, for search.'}
    },

    {'_type': 'repos', '_id': 'elasticsearch-py', '_op_type': 'update', 'doc': {
        'owner': {'name': u'Honza Král', 'email': 'honza.kral@gmail.com'},
        'created_at': datetime(2013, 5, 1, 16, 37, 32),
        'tags': ['elasticsearch', 'search', 'python', 'client'],
        'description': 'For searching snakes.'}
    },
]

if __name__ == '__main__':
    # get trace logger and set level
    tracer = logging.getLogger('elasticsearch.trace')
    tracer.setLevel(logging.INFO)
    tracer.addHandler(logging.FileHandler('/tmp/es_trace.log'))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H", "--host",
        action="store",
        default="localhost:9200",
        help="The elasticsearch host you wish to connect too. (Default: localhost:9200)")
    parser.add_argument(
        "-p", "--path",
        action="store",
        default=None,
        help="Path to git repo. Commits used as data to load into Elasticsearch. (Default: None")

    args = parser.parse_args()

    # instantiate es client, connects to localhost:9200 by default
    es = Elasticsearch(args.host)

    # we load the repo and all commits
    load_repo(es, path=args.path)

    # run the bulk operations
    success, _ = bulk(es, REPO_ACTIONS, index='git', raise_on_error=True)
    print('Performed %d actions' % success)

    # now we can retrieve the documents
    es_repo = es.get(index='git', doc_type='repos', id='elasticsearch')
    print('%s: %s' % (es_repo['_id'], es_repo['_source']['description']))

    # update - add java to es tags
    es.update(
        index='git',
        doc_type='repos',
        id='elasticsearch',
        body={
          "script": {
            "inline" : "ctx._source.tags.add(params.tag)",
            "params" : {
              "tag" : "java"
            }
          }
        }
    )

    # refresh to make the documents available for search
    es.indices.refresh(index='git')

    # and now we can count the documents
    print(es.count(index='git')['count'], 'documents in index')
