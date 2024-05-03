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

import pytest

from elasticsearch.helpers.vectorstore import (
    DenseVectorScriptScoreStrategy,
    DenseVectorStrategy,
    SparseVectorStrategy,
)


def test_sparse_vector_strategy_raises_errors():
    strategy = SparseVectorStrategy("my_model_id")

    with pytest.raises(ValueError):
        # missing query
        strategy.es_query(
            query=None,
            query_vector=None,
            text_field="text_field",
            vector_field="vector_field",
            k=10,
            num_candidates=20,
            filter=[],
        )

    with pytest.raises(ValueError):
        # query vector not allowed
        strategy.es_query(
            query="hi",
            query_vector=[1, 2, 3],
            text_field="text_field",
            vector_field="vector_field",
            k=10,
            num_candidates=20,
            filter=[],
        )


def test_dense_vector_strategy_raises_error():
    with pytest.raises(ValueError):
        # unknown distance
        DenseVectorStrategy(hybrid=True, text_field=None)

    with pytest.raises(ValueError):
        # unknown distance
        DenseVectorStrategy(distance="unknown distance").es_mappings_settings(
            text_field="text_field", vector_field="vector_field", num_dimensions=10
        )


def test_dense_vector_script_score_strategy_raises_error():
    with pytest.raises(ValueError):
        # missing query vector
        DenseVectorScriptScoreStrategy().es_query(
            query=None,
            query_vector=None,
            text_field="text_field",
            vector_field="vector_field",
            k=10,
            num_candidates=20,
            filter=[],
        )

    with pytest.raises(ValueError):
        # unknown distance
        DenseVectorScriptScoreStrategy(distance="unknown distance").es_query(
            query=None,
            query_vector=[1, 2, 3],
            text_field="text_field",
            vector_field="vector_field",
            k=10,
            num_candidates=20,
            filter=[],
        )
