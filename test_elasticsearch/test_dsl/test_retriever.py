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

from typing import Any

from pytest import raises

from elasticsearch.dsl import Search, query, retriever, types


def test_standard_to_dict() -> None:
    assert {"standard": {"query": {"match": {"title": "python"}}}} == (
        retriever.StandardRetriever(query=query.Match(title="python")).to_dict()
    )


def test_standard_expands_query_from_dict() -> None:
    # the dict form is accepted at runtime but not in the generated type hints
    r = retriever.StandardRetriever(query={"match": {"title": "python"}})  # type: ignore[arg-type]

    assert isinstance(r.query, query.Match)
    assert {"standard": {"query": {"match": {"title": "python"}}}} == r.to_dict()


def test_knn_to_dict() -> None:
    r = retriever.KnnRetriever(
        field="vector", query_vector=[1.0, 2.0], k=10, num_candidates=100
    )
    d = {
        "knn": {
            "field": "vector",
            "query_vector": [1.0, 2.0],
            "k": 10,
            "num_candidates": 100,
        }
    }

    assert d == r.to_dict()


def test_filter_is_a_multi_query() -> None:
    r = retriever.StandardRetriever(
        query=query.MatchAll(), filter=query.Term(published=True)
    )
    d = {
        "standard": {
            "query": {"match_all": {}},
            "filter": [{"term": {"published": True}}],
        }
    }

    assert d == r.to_dict()


def test_rrf_to_dict() -> None:
    r = retriever.RRFRetriever(
        retrievers=[
            retriever.StandardRetriever(query=query.Match(title="python")),
            retriever.KnnRetriever(
                field="vector", query_vector=[1.0], k=10, num_candidates=100
            ),
        ],
        rank_constant=60,
        rank_window_size=100,
    )
    d = {
        "rrf": {
            "retrievers": [
                {"standard": {"query": {"match": {"title": "python"}}}},
                {
                    "knn": {
                        "field": "vector",
                        "query_vector": [1.0],
                        "k": 10,
                        "num_candidates": 100,
                    }
                },
            ],
            "rank_constant": 60,
            "rank_window_size": 100,
        }
    }

    assert d == r.to_dict()


def test_rrf_retriever_component_with_weight_to_dict() -> None:
    """`retrievers` accepts RRFRetrieverComponent, which carries a weight."""
    r = retriever.RRFRetriever(
        retrievers=[
            types.RRFRetrieverComponent(
                retriever=retriever.StandardRetriever(
                    query=query.Match(title="python")
                ),
                weight=2.0,
            ),
            retriever.StandardRetriever(query=query.Match(body="python")),
        ],
    )
    d = {
        "rrf": {
            "retrievers": [
                {
                    "retriever": {
                        "standard": {"query": {"match": {"title": "python"}}}
                    },
                    "weight": 2.0,
                },
                {"standard": {"query": {"match": {"body": "python"}}}},
            ],
        }
    }

    assert d == r.to_dict()

    # the same component given as a raw dict
    raw_component: Any = {
        "retriever": {"standard": {"query": {"match": {"title": "python"}}}},
        "weight": 2.0,
    }
    r2 = retriever.RRFRetriever(
        retrievers=[
            raw_component,
            retriever.StandardRetriever(query=query.Match(body="python")),
        ],
    )

    assert d == r2.to_dict()


def test_rrf_component_keeps_nested_retriever_as_an_object() -> None:
    component = types.RRFRetrieverComponent(
        retriever={"standard": {"query": {"match": {"title": "python"}}}},  # type: ignore[arg-type]
        weight=2.0,
    )
    r = retriever.RRFRetriever(retrievers=[component])

    assert isinstance(r.retrievers[0].retriever, retriever.StandardRetriever)
    # the caller's component is not mutated
    assert component.retriever == {
        "standard": {"query": {"match": {"title": "python"}}}
    }


def test_linear_inner_retriever_to_dict() -> None:
    """`InnerRetriever` carries a weight too, and expands the same way."""
    r = retriever.LinearRetriever(
        retrievers=[
            types.InnerRetriever(
                retriever=retriever.StandardRetriever(
                    query=query.Match(title="python")
                ),
                weight=1.0,
                normalizer="minmax",
            ),
        ],
    )
    d = {
        "linear": {
            "retrievers": [
                {
                    "retriever": {
                        "standard": {"query": {"match": {"title": "python"}}}
                    },
                    "weight": 1.0,
                    "normalizer": "minmax",
                },
            ],
        }
    }

    assert d == r.to_dict()


def test_nested_retriever_to_dict() -> None:
    r = retriever.TextSimilarityRerankerRetriever(
        retriever=retriever.StandardRetriever(query=query.Match(title="python")),
        field="title",
        inference_text="python",
        inference_id="my-model",
    )
    d = {
        "text_similarity_reranker": {
            "retriever": {"standard": {"query": {"match": {"title": "python"}}}},
            "field": "title",
            "inference_text": "python",
            "inference_id": "my-model",
        }
    }

    assert d == r.to_dict()


def test_diversify_serializes_lambda_without_trailing_underscore() -> None:
    r = retriever.DiversifyRetriever(
        type="mmr",
        field="vector",
        retriever=retriever.StandardRetriever(query=query.MatchAll()),
        lambda_=0.5,
    )
    d = {
        "diversify": {
            "type": "mmr",
            "field": "vector",
            "retriever": {"standard": {"query": {"match_all": {}}}},
            "lambda": 0.5,
        }
    }

    assert d == r.to_dict()


def test_R_passes_retriever_through() -> None:
    r = retriever.StandardRetriever(query=query.MatchAll())

    assert retriever.R(r) is r


def test_R_constructs_retriever_by_name() -> None:
    r = retriever.R("standard", query=query.Match(title="python"))

    assert isinstance(r, retriever.StandardRetriever)
    assert {"standard": {"query": {"match": {"title": "python"}}}} == r.to_dict()


def test_R_constructs_retriever_from_dict() -> None:
    r = retriever.R({"standard": {"query": {"match": {"title": "python"}}}})

    assert isinstance(r, retriever.StandardRetriever)
    assert {"standard": {"query": {"match": {"title": "python"}}}} == r.to_dict()


def test_R_raises_error_when_passed_in_dict_and_params() -> None:
    with raises(ValueError):
        # Ignore types as it's not a valid call
        retriever.R({"standard": {}}, query=query.MatchAll())  # type: ignore[call-overload]


def test_R_raises_error_when_passed_in_retriever_and_params() -> None:
    r = retriever.StandardRetriever(query=query.MatchAll())

    with raises(ValueError):
        # Ignore types as it's not a valid call signature
        retriever.R(r, query=query.MatchAll())  # type: ignore[call-overload]


def test_R_raises_error_on_multi_key_dict() -> None:
    with raises(ValueError):
        retriever.R({"standard": {}, "knn": {}})


def test_R_raises_error_on_unknown_retriever() -> None:
    with raises(Exception):
        retriever.R("not_a_retriever", field="value")


def test_equality_and_repr() -> None:
    r = retriever.StandardRetriever(query=query.Match(title="python"))

    assert r == retriever.StandardRetriever(query=query.Match(title="python"))
    assert "StandardRetriever(query=Match(title='python'))" == repr(r)


def test_search_retriever_to_dict_and_clone() -> None:
    s = Search().retriever(
        retriever.StandardRetriever(query=query.Match(title="python"))
    )
    d = {"retriever": {"standard": {"query": {"match": {"title": "python"}}}}}

    assert s.to_dict() == d
    assert s._clone().to_dict() == d

    s2 = Search.from_dict(d)
    assert isinstance(s2._retriever, retriever.StandardRetriever)
    assert s2.to_dict() == d


def test_search_retriever_rejects_a_component() -> None:
    # a weighted component is only valid inside the `retrievers` list of
    # `rrf`/`linear`, never as the top-level retriever
    component = {"retriever": {"standard": {}}, "weight": 2.0}

    with raises(ValueError):
        Search().retriever(component)

    with raises(ValueError):
        Search.from_dict({"retriever": component})
