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
        "properties": {
            "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}}
        }
    }

    create_index_body = {
        "settings": {
            # just one shard, no replicas for testing
            "number_of_shards": 1,
            "number_of_replicas": 0,
            # custom analyzer for analyzing file paths
            "analysis": {
                "analyzer": {
                    "file_path": {
                        "type": "custom",
                        "tokenizer": "path_hierarchy",
                        "filter": ["lowercase"],
                    }
                }
            },
        },
        "mappings": {
            "doc": {
                "properties": {
                    "repository": {"type": "keyword"},
                    "author": user_mapping,
                    "authored_date": {"type": "date"},
                    "committer": user_mapping,
                    "committed_date": {"type": "date"},
                    "parent_shas": {"type": "keyword"},
                    "description": {"type": "text", "analyzer": "snowball"},
                    "files": {
                        "type": "text",
                        "analyzer": "file_path",
                        "fielddata": True,
                    },
                }
            }
        },
    }

    # create empty index
    try:
        client.indices.create(index=index, body=create_index_body)
    except TransportError as e:
        # ignore already existing index
        if e.error == "index_already_exists_exception":
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
            "_id": commit.hexsha,
            "repository": name,
            "committed_date": datetime.fromtimestamp(commit.committed_date),
            "committer": {
                "name": commit.committer.name,
                "email": commit.committer.email,
            },
            "authored_date": datetime.fromtimestamp(commit.authored_date),
            "author": {"name": commit.author.name, "email": commit.author.email},
            "description": commit.message,
            "parent_shas": [p.hexsha for p in commit.parents],
            # we only care about the filenames, not the per-file stats
            "files": list(commit.stats.files),
            "stats": commit.stats.total,
        }


def load_repo(client, path=None, index="git"):
    """
    Parse a git repository with all it's commits and load it into elasticsearch
    using `client`. If the index doesn't exist it will be created.
    """
    path = dirname(dirname(abspath(__file__))) if path is None else path
    repo_name = basename(path)
    repo = git.Repo(path)

    create_git_index(client, index)

    # we let the streaming bulk continuously process the commits as they come
    # in - since the `parse_commits` function is a generator this will avoid
    # loading all the commits into memory
    for ok, result in streaming_bulk(
        client,
        parse_commits(repo.refs.master.commit, repo_name),
        index=index,
        doc_type="doc",
        chunk_size=50,  # keep the batch sizes small for appearances only
    ):
        action, result = result.popitem()
        doc_id = "/%s/doc/%s" % (index, result["_id"])
        # process the information from ES whether the document has been
        # successfully indexed
        if not ok:
            print("Failed to %s document %s: %r" % (action, doc_id, result))
        else:
            print(doc_id)


# we manually update some documents to add additional information
UPDATES = [
    {
        "_type": "doc",
        "_id": "20fbba1230cabbc0f4644f917c6c2be52b8a63e8",
        "_op_type": "update",
        "doc": {"initial_commit": True},
    },
    {
        "_type": "doc",
        "_id": "ae0073c8ca7e24d237ffd56fba495ed409081bf4",
        "_op_type": "update",
        "doc": {"release": "5.0.0"},
    },
]

if __name__ == "__main__":
    # get trace logger and set level
    tracer = logging.getLogger("elasticsearch.trace")
    tracer.setLevel(logging.INFO)
    tracer.addHandler(logging.FileHandler("/tmp/es_trace.log"))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H",
        "--host",
        action="store",
        default="localhost:9200",
        help="The elasticsearch host you wish to connect to. (Default: localhost:9200)",
    )
    parser.add_argument(
        "-p",
        "--path",
        action="store",
        default=None,
        help="Path to git repo. Commits used as data to load into Elasticsearch. (Default: None",
    )

    args = parser.parse_args()

    # instantiate es client, connects to localhost:9200 by default
    es = Elasticsearch(args.host)

    # we load the repo and all commits
    load_repo(es, path=args.path)

    # run the bulk operations
    success, _ = bulk(es, UPDATES, index="git")
    print("Performed %d actions" % success)

    # we can now make docs visible for searching
    es.indices.refresh(index="git")

    # now we can retrieve the documents
    initial_commit = es.get(
        index="git", doc_type="doc", id="20fbba1230cabbc0f4644f917c6c2be52b8a63e8"
    )
    print(
        "%s: %s" % (initial_commit["_id"], initial_commit["_source"]["committed_date"])
    )

    # and now we can count the documents
    print(es.count(index="git")["count"], "documents in index")
