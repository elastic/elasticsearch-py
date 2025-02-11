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

from datetime import datetime, timedelta
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from typing_extensions import Self

from .aggs import A, Agg
from .query import MatchAll, Nested, Query, Range, Terms
from .response import Response
from .utils import _R, AttrDict

if TYPE_CHECKING:
    from .document_base import DocumentBase
    from .response.aggs import BucketData
    from .search_base import SearchBase

FilterValueType = Union[str, datetime, Sequence[str]]

__all__ = [
    "FacetedSearchBase",
    "HistogramFacet",
    "TermsFacet",
    "DateHistogramFacet",
    "RangeFacet",
    "NestedFacet",
]


class Facet(Generic[_R]):
    """
    A facet on faceted search. Wraps and aggregation and provides functionality
    to create a filter for selected values and return a list of facet values
    from the result of the aggregation.
    """

    agg_type: str = ""

    def __init__(
        self, metric: Optional[Agg[_R]] = None, metric_sort: str = "desc", **kwargs: Any
    ):
        self.filter_values = ()
        self._params = kwargs
        self._metric = metric
        if metric and metric_sort:
            self._params["order"] = {"metric": metric_sort}

    def get_aggregation(self) -> Agg[_R]:
        """
        Return the aggregation object.
        """
        agg: Agg[_R] = A(self.agg_type, **self._params)
        if self._metric:
            agg.metric("metric", self._metric)
        return agg

    def add_filter(self, filter_values: List[FilterValueType]) -> Optional[Query]:
        """
        Construct a filter.
        """
        if not filter_values:
            return None

        f = self.get_value_filter(filter_values[0])
        for v in filter_values[1:]:
            f |= self.get_value_filter(v)
        return f

    def get_value_filter(self, filter_value: FilterValueType) -> Query:  # type: ignore[empty-body]
        """
        Construct a filter for an individual value
        """
        pass

    def is_filtered(self, key: str, filter_values: List[FilterValueType]) -> bool:
        """
        Is a filter active on the given key.
        """
        return key in filter_values

    def get_value(self, bucket: "BucketData[_R]") -> Any:
        """
        return a value representing a bucket. Its key as default.
        """
        return bucket["key"]

    def get_metric(self, bucket: "BucketData[_R]") -> int:
        """
        Return a metric, by default doc_count for a bucket.
        """
        if self._metric:
            return cast(int, bucket["metric"]["value"])
        return cast(int, bucket["doc_count"])

    def get_values(
        self, data: "BucketData[_R]", filter_values: List[FilterValueType]
    ) -> List[Tuple[Any, int, bool]]:
        """
        Turn the raw bucket data into a list of tuples containing the key,
        number of documents and a flag indicating whether this value has been
        selected or not.
        """
        out = []
        for bucket in data.buckets:
            b = cast("BucketData[_R]", bucket)
            key = self.get_value(b)
            out.append((key, self.get_metric(b), self.is_filtered(key, filter_values)))
        return out


class TermsFacet(Facet[_R]):
    agg_type = "terms"

    def add_filter(self, filter_values: List[FilterValueType]) -> Optional[Query]:
        """Create a terms filter instead of bool containing term filters."""
        if filter_values:
            return Terms(self._params["field"], filter_values, _expand__to_dot=False)
        return None


class RangeFacet(Facet[_R]):
    agg_type = "range"

    def _range_to_dict(
        self, range: Tuple[Any, Tuple[Optional[int], Optional[int]]]
    ) -> Dict[str, Any]:
        key, _range = range
        out: Dict[str, Any] = {"key": key}
        if _range[0] is not None:
            out["from"] = _range[0]
        if _range[1] is not None:
            out["to"] = _range[1]
        return out

    def __init__(
        self,
        ranges: Sequence[Tuple[Any, Tuple[Optional[int], Optional[int]]]],
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._params["ranges"] = list(map(self._range_to_dict, ranges))
        self._params["keyed"] = False
        self._ranges = dict(ranges)

    def get_value_filter(self, filter_value: FilterValueType) -> Query:
        f, t = self._ranges[filter_value]
        limits: Dict[str, Any] = {}
        if f is not None:
            limits["gte"] = f
        if t is not None:
            limits["lt"] = t

        return Range(self._params["field"], limits, _expand__to_dot=False)


class HistogramFacet(Facet[_R]):
    agg_type = "histogram"

    def get_value_filter(self, filter_value: FilterValueType) -> Range:
        return Range(
            self._params["field"],
            {
                "gte": filter_value,
                "lt": filter_value + self._params["interval"],
            },
            _expand__to_dot=False,
        )


def _date_interval_year(d: datetime) -> datetime:
    return d.replace(
        year=d.year + 1, day=(28 if d.month == 2 and d.day == 29 else d.day)
    )


def _date_interval_month(d: datetime) -> datetime:
    return (d + timedelta(days=32)).replace(day=1)


def _date_interval_week(d: datetime) -> datetime:
    return d + timedelta(days=7)


def _date_interval_day(d: datetime) -> datetime:
    return d + timedelta(days=1)


def _date_interval_hour(d: datetime) -> datetime:
    return d + timedelta(hours=1)


class DateHistogramFacet(Facet[_R]):
    agg_type = "date_histogram"

    DATE_INTERVALS = {
        "year": _date_interval_year,
        "1Y": _date_interval_year,
        "month": _date_interval_month,
        "1M": _date_interval_month,
        "week": _date_interval_week,
        "1w": _date_interval_week,
        "day": _date_interval_day,
        "1d": _date_interval_day,
        "hour": _date_interval_hour,
        "1h": _date_interval_hour,
    }

    def __init__(self, **kwargs: Any):
        kwargs.setdefault("min_doc_count", 0)
        super().__init__(**kwargs)

    def get_value(self, bucket: "BucketData[_R]") -> Any:
        if not isinstance(bucket["key"], datetime):
            # Elasticsearch returns key=None instead of 0 for date 1970-01-01,
            # so we need to set key to 0 to avoid TypeError exception
            if bucket["key"] is None:
                bucket["key"] = 0
            # Preserve milliseconds in the datetime
            return datetime.utcfromtimestamp(int(cast(int, bucket["key"])) / 1000.0)
        else:
            return bucket["key"]

    def get_value_filter(self, filter_value: Any) -> Range:
        for interval_type in ("calendar_interval", "fixed_interval"):
            if interval_type in self._params:
                break
        else:
            interval_type = "interval"

        return Range(
            self._params["field"],
            {
                "gte": filter_value,
                "lt": self.DATE_INTERVALS[self._params[interval_type]](filter_value),
            },
            _expand__to_dot=False,
        )


class NestedFacet(Facet[_R]):
    agg_type = "nested"

    def __init__(self, path: str, nested_facet: Facet[_R]):
        self._path = path
        self._inner = nested_facet
        super().__init__(path=path, aggs={"inner": nested_facet.get_aggregation()})

    def get_values(
        self, data: "BucketData[_R]", filter_values: List[FilterValueType]
    ) -> List[Tuple[Any, int, bool]]:
        return self._inner.get_values(data.inner, filter_values)

    def add_filter(self, filter_values: List[FilterValueType]) -> Optional[Query]:
        inner_q = self._inner.add_filter(filter_values)
        if inner_q:
            return Nested(path=self._path, query=inner_q)
        return None


class FacetedResponse(Response[_R]):
    if TYPE_CHECKING:
        _faceted_search: "FacetedSearchBase[_R]"
        _facets: Dict[str, List[Tuple[Any, int, bool]]]

    @property
    def query_string(self) -> Optional[Union[str, Query]]:
        return self._faceted_search._query

    @property
    def facets(self) -> Dict[str, List[Tuple[Any, int, bool]]]:
        if not hasattr(self, "_facets"):
            super(AttrDict, self).__setattr__("_facets", AttrDict({}))
            for name, facet in self._faceted_search.facets.items():
                self._facets[name] = facet.get_values(
                    getattr(getattr(self.aggregations, "_filter_" + name), name),
                    self._faceted_search.filter_values.get(name, []),
                )
        return self._facets


class FacetedSearchBase(Generic[_R]):
    """
    Abstraction for creating faceted navigation searches that takes care of
    composing the queries, aggregations and filters as needed as well as
    presenting the results in an easy-to-consume fashion::

        class BlogSearch(FacetedSearch):
            index = 'blogs'
            doc_types = [Blog, Post]
            fields = ['title^5', 'category', 'description', 'body']

            facets = {
                'type': TermsFacet(field='_type'),
                'category': TermsFacet(field='category'),
                'weekly_posts': DateHistogramFacet(field='published_from', interval='week')
            }

            def search(self):
                ' Override search to add your own filters '
                s = super(BlogSearch, self).search()
                return s.filter('term', published=True)

        # when using:
        blog_search = BlogSearch("web framework", filters={"category": "python"})

        # supports pagination
        blog_search[10:20]

        response = blog_search.execute()

        # easy access to aggregation results:
        for category, hit_count, is_selected in response.facets.category:
            print(
                "Category %s has %d hits%s." % (
                    category,
                    hit_count,
                    ' and is chosen' if is_selected else ''
                )
            )

    """

    index: Optional[str] = None
    doc_types: Optional[List[Union[str, Type["DocumentBase"]]]] = None
    fields: Sequence[str] = []
    facets: Dict[str, Facet[_R]] = {}
    using = "default"

    if TYPE_CHECKING:

        def search(self) -> "SearchBase[_R]": ...

    def __init__(
        self,
        query: Optional[Union[str, Query]] = None,
        filters: Dict[str, FilterValueType] = {},
        sort: Sequence[str] = [],
    ):
        """
        :arg query: the text to search for
        :arg filters: facet values to filter
        :arg sort: sort information to be passed to :class:`~elasticsearch.dsl.Search`
        """
        self._query = query
        self._filters: Dict[str, Query] = {}
        self._sort = sort
        self.filter_values: Dict[str, List[FilterValueType]] = {}
        for name, value in filters.items():
            self.add_filter(name, value)

        self._s = self.build_search()

    def __getitem__(self, k: Union[int, slice]) -> Self:
        self._s = self._s[k]
        return self

    def add_filter(
        self, name: str, filter_values: Union[FilterValueType, List[FilterValueType]]
    ) -> None:
        """
        Add a filter for a facet.
        """
        # normalize the value into a list
        if not isinstance(filter_values, (tuple, list)):
            if filter_values is None:
                return
            filter_values = [
                filter_values,
            ]

        # remember the filter values for use in FacetedResponse
        self.filter_values[name] = filter_values  # type: ignore[assignment]

        # get the filter from the facet
        f = self.facets[name].add_filter(filter_values)  # type: ignore[arg-type]
        if f is None:
            return

        self._filters[name] = f

    def query(
        self, search: "SearchBase[_R]", query: Union[str, Query]
    ) -> "SearchBase[_R]":
        """
        Add query part to ``search``.

        Override this if you wish to customize the query used.
        """
        if query:
            if self.fields:
                return search.query("multi_match", fields=self.fields, query=query)
            else:
                return search.query("multi_match", query=query)
        return search

    def aggregate(self, search: "SearchBase[_R]") -> None:
        """
        Add aggregations representing the facets selected, including potential
        filters.
        """
        for f, facet in self.facets.items():
            agg = facet.get_aggregation()
            agg_filter: Query = MatchAll()
            for field, filter in self._filters.items():
                if f == field:
                    continue
                agg_filter &= filter
            search.aggs.bucket("_filter_" + f, "filter", filter=agg_filter).bucket(
                f, agg
            )

    def filter(self, search: "SearchBase[_R]") -> "SearchBase[_R]":
        """
        Add a ``post_filter`` to the search request narrowing the results based
        on the facet filters.
        """
        if not self._filters:
            return search

        post_filter: Query = MatchAll()
        for f in self._filters.values():
            post_filter &= f
        return search.post_filter(post_filter)

    def highlight(self, search: "SearchBase[_R]") -> "SearchBase[_R]":
        """
        Add highlighting for all the fields
        """
        return search.highlight(
            *(f if "^" not in f else f.split("^", 1)[0] for f in self.fields)
        )

    def sort(self, search: "SearchBase[_R]") -> "SearchBase[_R]":
        """
        Add sorting information to the request.
        """
        if self._sort:
            search = search.sort(*self._sort)
        return search

    def params(self, **kwargs: Any) -> None:
        """
        Specify query params to be used when executing the search. All the
        keyword arguments will override the current values. See
        https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.search
        for all available parameters.
        """
        self._s = self._s.params(**kwargs)

    def build_search(self) -> "SearchBase[_R]":
        """
        Construct the ``Search`` object.
        """
        s = self.search()
        if self._query is not None:
            s = self.query(s, self._query)
        s = self.filter(s)
        if self.fields:
            s = self.highlight(s)
        s = self.sort(s)
        self.aggregate(s)
        return s
