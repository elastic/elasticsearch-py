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

import collections.abc
from copy import deepcopy
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Literal,
    Mapping,
    MutableMapping,
    Optional,
    Protocol,
    Sequence,
    TypeVar,
    Union,
    cast,
    overload,
)

from elastic_transport.client_utils import DEFAULT

from .query import Query
from .utils import AttrDict, DslBase

if TYPE_CHECKING:
    from elastic_transport.client_utils import DefaultType

    from . import types
    from .document_base import InstrumentedField

_T = TypeVar("_T")
_M = TypeVar("_M", bound=Mapping[str, Any])


class RProxiedProtocol(Protocol[_T]):
    _proxied: _T


@overload
def R(
    name_or_retriever: MutableMapping[str, _M],
) -> Union["Retriever", "AttrDict[Any]"]: ...


@overload
def R(name_or_retriever: "Retriever") -> "Retriever": ...


@overload
def R(name_or_retriever: RProxiedProtocol[_T]) -> _T: ...


@overload
def R(name_or_retriever: str, **params: Any) -> "Retriever": ...


def R(
    name_or_retriever: Union[
        str,
        "Retriever",
        RProxiedProtocol[_T],
        MutableMapping[str, _M],
    ],
    **params: Any,
) -> Union["Retriever", "AttrDict[Any]", _T]:
    # types.RRFRetrieverComponent(retriever=..., weight=2.0)
    if isinstance(name_or_retriever, AttrDict):
        name_or_retriever = name_or_retriever.to_dict()

    # {"standard": {"query": {"match": {"title": "python"}}}}
    if isinstance(name_or_retriever, collections.abc.MutableMapping):
        if params:
            raise ValueError("R() cannot accept parameters when passing in a dict.")

        # RRF/Linear special case: {"retriever": {"standard": {...}}, "weight": 2.0}
        if "retriever" in name_or_retriever:
            component = RetrieverComponent(deepcopy(dict(name_or_retriever)))
            component.retriever = R(component.retriever)
            return component

        if len(name_or_retriever) != 1:
            raise ValueError(
                "R() can only accept dict with a single retriever "
                '({"standard": {...}}). '
                "Instead it got (%r)" % name_or_retriever
            )
        name, r_params = deepcopy(name_or_retriever).popitem()
        return Retriever.get_dsl_class(name)(_expand__to_dot=False, **r_params)

    # StandardRetriever()
    if isinstance(name_or_retriever, Retriever):
        if params:
            raise ValueError(
                "R() cannot accept parameters when passing in a Retriever object."
            )
        return name_or_retriever

    # s.retriever = R("standard", query=s.query)
    if hasattr(name_or_retriever, "_proxied"):
        return cast(RProxiedProtocol[_T], name_or_retriever)._proxied

    # "standard", query={"match": {"title": "python"}}
    return Retriever.get_dsl_class(name_or_retriever)(**params)


def _as_retriever(name_or_retriever: Union["Retriever", Dict[str, Any]]) -> "Retriever":
    """Coerce to a `Retriever`, for positions where a component is not valid.

    `R()` also returns a `RetrieverComponent` for dicts with a "retriever" key,
    which is only legitimate inside the `retrievers` list of `rrf` and `linear`.
    """
    r = R(name_or_retriever)
    if not isinstance(r, Retriever):
        raise ValueError(f"Expected a retriever, got {r!r}")
    return r


class Retriever(DslBase):
    _type_name = "retriever"
    _type_shortcut = staticmethod(R)
    name: ClassVar[Optional[str]] = None


class RetrieverComponent(AttrDict[Any]):
    """A retriever paired with a weight, as accepted by the `rrf` retriever.
    Also a retriever with a weight and/or normalizer as with `linear` retriever.

    Unlike a plain `AttrDict`, this serializes recursively so that the nested
    retriever is expanded rather than left as an object.
    """

    def to_dict(self, recursive: bool = True) -> Dict[str, Any]:
        return super().to_dict(recursive=recursive)


class StandardRetriever(Retriever):
    """
    A retriever that replaces the functionality of a traditional query.

    :arg query: Defines a query to retrieve a set of top documents.
    :arg search_after: Defines a search after object parameter used for
        pagination.
    :arg terminate_after: Maximum number of documents to collect for each
        shard.
    :arg sort: A sort object that that specifies the order of matching
        documents.
    :arg collapse: Collapses the top documents by a specified key into a
        single top document per key.
    :arg filter: Query to filter the documents that can match.
    :arg min_score: Minimum _score for matching documents. Documents with
        a lower _score are not included in the top documents.
    :arg _name: Retriever name.
    """

    name = "standard"
    _param_defs = {
        "query": {"type": "query"},
        "filter": {"type": "query", "multi": True},
    }

    def __init__(
        self,
        *,
        query: Union[Query, "DefaultType"] = DEFAULT,
        search_after: Union[
            Sequence[Union[int, float, str, bool, None]], "DefaultType"
        ] = DEFAULT,
        terminate_after: Union[int, "DefaultType"] = DEFAULT,
        sort: Union[
            Union[Union[str, "InstrumentedField"], "types.SortOptions"],
            Sequence[Union[Union[str, "InstrumentedField"], "types.SortOptions"]],
            Dict[str, Any],
            "DefaultType",
        ] = DEFAULT,
        collapse: Union["types.FieldCollapse", Dict[str, Any], "DefaultType"] = DEFAULT,
        filter: Union[Query, Sequence[Query], "DefaultType"] = DEFAULT,
        min_score: Union[float, "DefaultType"] = DEFAULT,
        _name: Union[str, "DefaultType"] = DEFAULT,
        **kwargs: Any,
    ):
        super().__init__(
            query=query,
            search_after=search_after,
            terminate_after=terminate_after,
            sort=sort,
            collapse=collapse,
            filter=filter,
            min_score=min_score,
            _name=_name,
            **kwargs,
        )


class KnnRetriever(Retriever):
    """
    A retriever that replaces the functionality  of a knn search.

    :arg field: (required) The name of the vector field to search against.
    :arg k: (required) Number of nearest neighbors to return as top hits.
    :arg num_candidates: (required) Number of nearest neighbor candidates
        to consider per shard.
    :arg query_vector: Query vector. Must have the same number of
        dimensions as the vector field you are searching against. You must
        provide a query_vector_builder or query_vector, but not both.
    :arg query_vector_builder: Defines a model to build a query vector.
    :arg visit_percentage: The percentage of vectors to explore per shard
        while doing knn search with bbq_disk
    :arg similarity: The minimum similarity required for a document to be
        considered a match.
    :arg rescore_vector: Apply oversampling and rescoring to quantized
        vectors
    :arg filter: Query to filter the documents that can match.
    :arg min_score: Minimum _score for matching documents. Documents with
        a lower _score are not included in the top documents.
    :arg _name: Retriever name.
    """

    name = "knn"
    _param_defs = {
        "filter": {"type": "query", "multi": True},
    }

    def __init__(
        self,
        *,
        field: Union[str, "DefaultType"] = DEFAULT,
        k: Union[int, "DefaultType"] = DEFAULT,
        num_candidates: Union[int, "DefaultType"] = DEFAULT,
        query_vector: Union[Sequence[float], "DefaultType"] = DEFAULT,
        query_vector_builder: Union[
            "types.QueryVectorBuilder", Dict[str, Any], "DefaultType"
        ] = DEFAULT,
        visit_percentage: Union[float, "DefaultType"] = DEFAULT,
        similarity: Union[float, "DefaultType"] = DEFAULT,
        rescore_vector: Union[
            "types.RescoreVector", Dict[str, Any], "DefaultType"
        ] = DEFAULT,
        filter: Union[Query, Sequence[Query], "DefaultType"] = DEFAULT,
        min_score: Union[float, "DefaultType"] = DEFAULT,
        _name: Union[str, "DefaultType"] = DEFAULT,
        **kwargs: Any,
    ):
        super().__init__(
            field=field,
            k=k,
            num_candidates=num_candidates,
            query_vector=query_vector,
            query_vector_builder=query_vector_builder,
            visit_percentage=visit_percentage,
            similarity=similarity,
            rescore_vector=rescore_vector,
            filter=filter,
            min_score=min_score,
            _name=_name,
            **kwargs,
        )


class RRFRetriever(Retriever):
    """
    A retriever that produces top documents from reciprocal rank fusion
    (RRF).

    :arg retrievers: (required) A list of child retrievers to specify
        which sets of returned top documents will have the RRF formula
        applied to them. Each retriever can optionally include a weight
        parameter.
    :arg rank_constant: This value determines how much influence documents
        in individual result sets per query have over the final ranked
        result set.
    :arg rank_window_size: This value determines the size of the
        individual result sets per query.
    :arg query:
    :arg fields:
    :arg filter: Query to filter the documents that can match.
    :arg min_score: Minimum _score for matching documents. Documents with
        a lower _score are not included in the top documents.
    :arg _name: Retriever name.
    """

    name = "rrf"
    _param_defs = {
        "retrievers": {"type": "retriever", "multi": True},
        "filter": {"type": "query", "multi": True},
    }

    def __init__(
        self,
        *,
        retrievers: Union[
            Sequence[Union[Retriever, "types.RRFRetrieverComponent"]],
            Dict[str, Any],
            "DefaultType",
        ] = DEFAULT,
        rank_constant: Union[int, "DefaultType"] = DEFAULT,
        rank_window_size: Union[int, "DefaultType"] = DEFAULT,
        query: Union[str, "DefaultType"] = DEFAULT,
        fields: Union[Sequence[str], "DefaultType"] = DEFAULT,
        filter: Union[Query, Sequence[Query], "DefaultType"] = DEFAULT,
        min_score: Union[float, "DefaultType"] = DEFAULT,
        _name: Union[str, "DefaultType"] = DEFAULT,
        **kwargs: Any,
    ):
        super().__init__(
            retrievers=retrievers,
            rank_constant=rank_constant,
            rank_window_size=rank_window_size,
            query=query,
            fields=fields,
            filter=filter,
            min_score=min_score,
            _name=_name,
            **kwargs,
        )


class TextSimilarityRerankerRetriever(Retriever):
    """
    A retriever that reranks the top documents based on a reranking model
    using the InferenceAPI

    :arg retriever: (required) The nested retriever which will produce the
        first-level results, that will later be used for reranking.
    :arg inference_text: (required) The text snippet used as the basis for
        similarity comparison.
    :arg field: (required) The document field to be used for text
        similarity comparisons. This field should contain the text that
        will be evaluated against the inference_text.
    :arg rank_window_size: This value determines how many documents we
        will consider from the nested retriever.
    :arg inference_id: Unique identifier of the inference endpoint created
        using the inference API.
    :arg chunk_rescorer: Whether to rescore on only the best matching
        chunks.
    :arg filter: Query to filter the documents that can match.
    :arg min_score: Minimum _score for matching documents. Documents with
        a lower _score are not included in the top documents.
    :arg _name: Retriever name.
    """

    name = "text_similarity_reranker"
    _param_defs = {
        "retriever": {"type": "retriever"},
        "filter": {"type": "query", "multi": True},
    }

    def __init__(
        self,
        *,
        retriever: Union[Retriever, "DefaultType"] = DEFAULT,
        inference_text: Union[str, "DefaultType"] = DEFAULT,
        field: Union[str, "DefaultType"] = DEFAULT,
        rank_window_size: Union[int, "DefaultType"] = DEFAULT,
        inference_id: Union[str, "DefaultType"] = DEFAULT,
        chunk_rescorer: Union[
            "types.ChunkRescorer", Dict[str, Any], "DefaultType"
        ] = DEFAULT,
        filter: Union[Query, Sequence[Query], "DefaultType"] = DEFAULT,
        min_score: Union[float, "DefaultType"] = DEFAULT,
        _name: Union[str, "DefaultType"] = DEFAULT,
        **kwargs: Any,
    ):
        super().__init__(
            retriever=retriever,
            inference_text=inference_text,
            field=field,
            rank_window_size=rank_window_size,
            inference_id=inference_id,
            chunk_rescorer=chunk_rescorer,
            filter=filter,
            min_score=min_score,
            _name=_name,
            **kwargs,
        )


class RuleRetriever(Retriever):
    """
    A retriever that replaces the functionality of a rule query.

    :arg ruleset_ids: (required) The ruleset IDs containing the rules this
        retriever is evaluating against.
    :arg match_criteria: (required) The match criteria that will determine
        if a rule in the provided rulesets should be applied.
    :arg retriever: (required) The retriever whose results rules should be
        applied to.
    :arg rank_window_size: This value determines the size of the
        individual result set.
    :arg filter: Query to filter the documents that can match.
    :arg min_score: Minimum _score for matching documents. Documents with
        a lower _score are not included in the top documents.
    :arg _name: Retriever name.
    """

    name = "rule"
    _param_defs = {
        "retriever": {"type": "retriever"},
        "filter": {"type": "query", "multi": True},
    }

    def __init__(
        self,
        *,
        ruleset_ids: Union[str, Sequence[str], "DefaultType"] = DEFAULT,
        match_criteria: Any = DEFAULT,
        retriever: Union[Retriever, "DefaultType"] = DEFAULT,
        rank_window_size: Union[int, "DefaultType"] = DEFAULT,
        filter: Union[Query, Sequence[Query], "DefaultType"] = DEFAULT,
        min_score: Union[float, "DefaultType"] = DEFAULT,
        _name: Union[str, "DefaultType"] = DEFAULT,
        **kwargs: Any,
    ):
        super().__init__(
            ruleset_ids=ruleset_ids,
            match_criteria=match_criteria,
            retriever=retriever,
            rank_window_size=rank_window_size,
            filter=filter,
            min_score=min_score,
            _name=_name,
            **kwargs,
        )


class RescorerRetriever(Retriever):
    """
    A retriever that re-scores only the results produced by its child
    retriever.

    :arg retriever: (required) Inner retriever.
    :arg rescore: (required)
    :arg filter: Query to filter the documents that can match.
    :arg min_score: Minimum _score for matching documents. Documents with
        a lower _score are not included in the top documents.
    :arg _name: Retriever name.
    """

    name = "rescorer"
    _param_defs = {
        "retriever": {"type": "retriever"},
        "filter": {"type": "query", "multi": True},
    }

    def __init__(
        self,
        *,
        retriever: Union[Retriever, "DefaultType"] = DEFAULT,
        rescore: Union[
            "types.Rescore",
            Sequence["types.Rescore"],
            Sequence[Dict[str, Any]],
            "DefaultType",
        ] = DEFAULT,
        filter: Union[Query, Sequence[Query], "DefaultType"] = DEFAULT,
        min_score: Union[float, "DefaultType"] = DEFAULT,
        _name: Union[str, "DefaultType"] = DEFAULT,
        **kwargs: Any,
    ):
        super().__init__(
            retriever=retriever,
            rescore=rescore,
            filter=filter,
            min_score=min_score,
            _name=_name,
            **kwargs,
        )


class LinearRetriever(Retriever):
    """
    A retriever that supports the combination of different retrievers
    through a weighted linear combination.

    :arg retrievers: Inner retrievers.
    :arg rank_window_size:
    :arg query:
    :arg fields:
    :arg normalizer:
    :arg filter: Query to filter the documents that can match.
    :arg min_score: Minimum _score for matching documents. Documents with
        a lower _score are not included in the top documents.
    :arg _name: Retriever name.
    """

    name = "linear"
    _param_defs = {
        "retrievers": {"type": "retriever", "multi": True},
        "filter": {"type": "query", "multi": True},
    }

    def __init__(
        self,
        *,
        retrievers: Union[
            Sequence["types.InnerRetriever"], Sequence[Dict[str, Any]], "DefaultType"
        ] = DEFAULT,
        rank_window_size: Union[int, "DefaultType"] = DEFAULT,
        query: Union[str, "DefaultType"] = DEFAULT,
        fields: Union[Sequence[str], "DefaultType"] = DEFAULT,
        normalizer: Union[
            Literal["none", "minmax", "l2_norm"], "DefaultType"
        ] = DEFAULT,
        filter: Union[Query, Sequence[Query], "DefaultType"] = DEFAULT,
        min_score: Union[float, "DefaultType"] = DEFAULT,
        _name: Union[str, "DefaultType"] = DEFAULT,
        **kwargs: Any,
    ):
        super().__init__(
            retrievers=retrievers,
            rank_window_size=rank_window_size,
            query=query,
            fields=fields,
            normalizer=normalizer,
            filter=filter,
            min_score=min_score,
            _name=_name,
            **kwargs,
        )


class PinnedRetriever(Retriever):
    """
    A pinned retriever applies pinned documents to the underlying
    retriever. This retriever will rewrite to a PinnedQueryBuilder.

    :arg retriever: (required) Inner retriever.
    :arg ids:
    :arg docs:
    :arg rank_window_size:
    :arg filter: Query to filter the documents that can match.
    :arg min_score: Minimum _score for matching documents. Documents with
        a lower _score are not included in the top documents.
    :arg _name: Retriever name.
    """

    name = "pinned"
    _param_defs = {
        "retriever": {"type": "retriever"},
        "filter": {"type": "query", "multi": True},
    }

    def __init__(
        self,
        *,
        retriever: Union[Retriever, "DefaultType"] = DEFAULT,
        ids: Union[Sequence[str], "DefaultType"] = DEFAULT,
        docs: Union[
            Sequence["types.SpecifiedDocument"], Sequence[Dict[str, Any]], "DefaultType"
        ] = DEFAULT,
        rank_window_size: Union[int, "DefaultType"] = DEFAULT,
        filter: Union[Query, Sequence[Query], "DefaultType"] = DEFAULT,
        min_score: Union[float, "DefaultType"] = DEFAULT,
        _name: Union[str, "DefaultType"] = DEFAULT,
        **kwargs: Any,
    ):
        super().__init__(
            retriever=retriever,
            ids=ids,
            docs=docs,
            rank_window_size=rank_window_size,
            filter=filter,
            min_score=min_score,
            _name=_name,
            **kwargs,
        )


class DiversifyRetriever(Retriever):
    """
    A retriever that diversifies the results from its child retriever.

    :arg type: (required) The diversification strategy to apply.
    :arg field: (required) The document field on which to diversify
        results on.
    :arg retriever: (required) The nested retriever whose results will be
        diversified.
    :arg size: The number of top documents to return after
        diversification.
    :arg rank_window_size: The number of top documents from the nested
        retriever to consider for diversification.
    :arg query_vector: The query vector used for diversification.
    :arg query_vector_builder: a dense vector query vector builder to use
        instead of a static query_vector
    :arg lambda: Controls the trade-off between relevance and diversity
        for MMR. A value of 0.0 focuses solely on diversity, while a value
        of 1.0 focuses solely on relevance. Required for MMR
    :arg filter: Query to filter the documents that can match.
    :arg min_score: Minimum _score for matching documents. Documents with
        a lower _score are not included in the top documents.
    :arg _name: Retriever name.
    """

    name = "diversify"
    _param_defs = {
        "retriever": {"type": "retriever"},
        "filter": {"type": "query", "multi": True},
    }

    def __init__(
        self,
        *,
        type: Union[Literal["mmr"], "DefaultType"] = DEFAULT,
        field: Union[str, "DefaultType"] = DEFAULT,
        retriever: Union[Retriever, "DefaultType"] = DEFAULT,
        size: Union[int, "DefaultType"] = DEFAULT,
        rank_window_size: Union[int, "DefaultType"] = DEFAULT,
        query_vector: Union[Sequence[float], "DefaultType"] = DEFAULT,
        query_vector_builder: Union[
            "types.QueryVectorBuilder", Dict[str, Any], "DefaultType"
        ] = DEFAULT,
        lambda_: Union[float, "DefaultType"] = DEFAULT,
        filter: Union[Query, Sequence[Query], "DefaultType"] = DEFAULT,
        min_score: Union[float, "DefaultType"] = DEFAULT,
        _name: Union[str, "DefaultType"] = DEFAULT,
        **kwargs: Any,
    ):
        super().__init__(
            type=type,
            field=field,
            retriever=retriever,
            size=size,
            rank_window_size=rank_window_size,
            query_vector=query_vector,
            query_vector_builder=query_vector_builder,
            lambda_=lambda_,
            filter=filter,
            min_score=min_score,
            _name=_name,
            **kwargs,
        )
