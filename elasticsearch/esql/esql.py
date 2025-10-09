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

import json
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from ..dsl.document_base import DocumentBase, InstrumentedExpression, InstrumentedField

FieldType = Union[InstrumentedField, str]
IndexType = Union[Type[DocumentBase], str]
ExpressionType = Any


class ESQL(ABC):
    """The static methods of the ``ESQL`` class provide access to the ES|QL source
    commands, used to create ES|QL queries.

    These methods return an instance of class ``ESQLBase``, which provides access to
    the ES|QL processing commands.
    """

    @staticmethod
    def from_(*indices: IndexType) -> "From":
        """The ``FROM`` source command returns a table with data from a data stream, index, or alias.

        :param indices: A list of indices, data streams or aliases. Supports wildcards and date math.

        Examples::

            query1 = ESQL.from_("employees")
            query2 = ESQL.from_("<logs-{now/d}>")
            query3 = ESQL.from_("employees-00001", "other-employees-*")
            query4 = ESQL.from_("cluster_one:employees-00001", "cluster_two:other-employees-*")
            query5 = ESQL.from_("employees").metadata("_id")
        """
        return From(*indices)

    @staticmethod
    def row(**params: ExpressionType) -> "Row":
        """The ``ROW`` source command produces a row with one or more columns with values that you specify.
        This can be useful for testing.

        :param params: the column values to produce, given as keyword arguments.

        Examples::

            query1 = ESQL.row(a=1, b="two", c=None)
            query2 = ESQL.row(a=[1, 2])
            query3 = ESQL.row(a=functions.round(1.23, 0))
        """
        return Row(**params)

    @staticmethod
    def show(item: str) -> "Show":
        """The ``SHOW`` source command returns information about the deployment and its capabilities.

        :param item: Can only be ``INFO``.

        Examples::

            query = ESQL.show("INFO")
        """
        return Show(item)

    @staticmethod
    def ts(*indices: IndexType) -> "TS":
        """The ``TS`` source command is similar to ``FROM``, but for time series indices.

        :param indices: A list of indices, data streams or aliases. Supports wildcards and date math.

        Examples::

            query = (
                ESQL.ts("metrics")
                .where("@timestamp >= now() - 1 day")
                .stats("SUM(AVG_OVER_TIME(memory_usage)").by("host", "TBUCKET(1 hour)")
            )
        """
        return TS(*indices)

    @staticmethod
    def branch() -> "Branch":
        """This method can only be used inside a ``FORK`` command to create each branch.

        Examples::

            query = ESQL.from_("employees").fork(
                ESQL.branch().where("emp_no == 10001"),
                ESQL.branch().where("emp_no == 10002"),
            )
        """
        return Branch()


class ESQLBase(ABC):
    """The methods of the ``ESQLBase`` class provide access to the ES|QL processing
    commands, used to build ES|QL queries.
    """

    def __init__(self, parent: Optional["ESQLBase"] = None):
        self._parent = parent

    def __repr__(self) -> str:
        return self.render()

    def render(self) -> str:
        return (
            self._parent.render() + "\n| " if self._parent else ""
        ) + self._render_internal()

    @abstractmethod
    def _render_internal(self) -> str:
        pass

    @staticmethod
    def _format_index(index: IndexType) -> str:
        return index._index._name if hasattr(index, "_index") else str(index)

    @staticmethod
    def _format_id(id: FieldType, allow_patterns: bool = False) -> str:
        s = str(id)  # in case it is an InstrumentedField
        if allow_patterns and "*" in s:
            return s  # patterns cannot be escaped
        if re.fullmatch(r"[a-zA-Z_@][a-zA-Z0-9_\.]*", s):
            return s
        # this identifier needs to be escaped
        s.replace("`", "``")
        return f"`{s}`"

    @staticmethod
    def _format_expr(expr: ExpressionType) -> str:
        return (
            json.dumps(expr)
            if not isinstance(expr, (str, InstrumentedExpression))
            else str(expr)
        )

    def _is_forked(self) -> bool:
        if self.__class__.__name__ == "Fork":
            return True
        if self._parent:
            return self._parent._is_forked()
        return False

    def change_point(self, value: FieldType) -> "ChangePoint":
        """``CHANGE_POINT`` detects spikes, dips, and change points in a metric.

        :param value: The column with the metric in which you want to detect a change point.

        Examples::

            query = (
                ESQL.row(key=list(range(1, 26)))
                .mv_expand("key")
                .eval(value=functions.case("key<13", 0, 42))
                .change_point("value")
                .on("key")
                .where("type IS NOT NULL")
            )
        """
        return ChangePoint(self, value)

    def completion(
        self, *prompt: ExpressionType, **named_prompt: ExpressionType
    ) -> "Completion":
        """The ``COMPLETION`` command allows you to send prompts and context to a Large
        Language Model (LLM) directly within your ES|QL queries, to perform text
        generation tasks.

        :param prompt: The input text or expression used to prompt the LLM. This can
                       be a string literal or a reference to a column containing text.
        :param named_prompt: The input text or expresion, given as a keyword argument.
                             The argument name is used for the column name. If the
                             prompt is given as a positional argument, the results will
                             be stored in a column named ``completion``. If the
                             specified column already exists, it will be overwritten
                             with the new results.

        Examples::

            query1 = (
                ESQL.row(question="What is Elasticsearch?")
                .completion("question").with_("test_completion_model")
                .keep("question", "completion")
            )
            query2 = (
                ESQL.row(question="What is Elasticsearch?")
                .completion(answer="question").with_("test_completion_model")
                .keep("question", "answer")
            )
            query3 = (
                ESQL.from_("movies")
                .sort("rating DESC")
                .limit(10)
                .eval(prompt=\"\"\"CONCAT(
                    "Summarize this movie using the following information: \\n",
                    "Title: ", title, "\\n",
                    "Synopsis: ", synopsis, "\\n",
                    "Actors: ", MV_CONCAT(actors, ", "), "\\n",
                )\"\"\")
                .completion(summary="prompt").with_("test_completion_model")
                .keep("title", "summary", "rating")
            )
        """
        return Completion(self, *prompt, **named_prompt)

    def dissect(self, input: FieldType, pattern: str) -> "Dissect":
        """``DISSECT`` enables you to extract structured data out of a string.

        :param input: The column that contains the string you want to structure. If
                      the column has multiple values, ``DISSECT`` will process each value.
        :param pattern: A dissect pattern. If a field name conflicts with an existing
                        column, the existing column is dropped. If a field name is used
                        more than once, only the rightmost duplicate creates a column.

        Examples::

            query = (
                ESQL.row(a="2023-01-23T12:15:00.000Z - some text - 127.0.0.1")
                .dissect("a", "%{date} - %{msg} - %{ip}")
                .keep("date", "msg", "ip")
                .eval(date="TO_DATETIME(date)")
            )
        """
        return Dissect(self, input, pattern)

    def drop(self, *columns: FieldType) -> "Drop":
        """The ``DROP`` processing command removes one or more columns.

        :param columns: The columns to drop, given as positional arguments. Supports wildcards.

        Examples::

            query1 = ESQL.from_("employees").drop("height")
            query2 = ESQL.from_("employees").drop("height*")
        """
        return Drop(self, *columns)

    def enrich(self, policy: str) -> "Enrich":
        """``ENRICH`` enables you to add data from existing indices as new columns using an
        enrich policy.

        :param policy: The name of the enrich policy. You need to create and execute the
                       enrich policy first.

        Examples::

            query1 = (
                ESQL.row(a="1")
                .enrich("languages_policy").on("a").with_("language_name")
            )
            query2 = (
                ESQL.row(a="1")
                .enrich("languages_policy").on("a").with_(name="language_name")
            )
        """
        return Enrich(self, policy)

    def eval(self, *columns: ExpressionType, **named_columns: ExpressionType) -> "Eval":
        """The ``EVAL`` processing command enables you to append new columns with calculated values.

        :param columns: The values for the columns, given as positional arguments. Can be literals,
                        expressions, or functions. Can use columns defined left of this one.
        :param named_columns: The values for the new columns, given as keyword arguments. The name
                              of the arguments is used as column name. If a column with the same
                              name already exists, the existing column is dropped. If a column name
                              is used more than once, only the rightmost duplicate creates a column.

        Examples::

            query1 = (
                ESQL.from_("employees")
                .sort("emp_no")
                .keep("first_name", "last_name", "height")
                .eval(height_feet="height * 3.281", height_cm="height * 100")
            )
            query2 = (
                ESQL.from_("employees")
                .eval("height * 3.281")
                .stats(avg_height_feet=functions.avg("`height * 3.281`"))
            )
        """
        return Eval(self, *columns, **named_columns)

    def fork(
        self,
        fork1: "Branch",
        fork2: Optional["Branch"] = None,
        fork3: Optional["Branch"] = None,
        fork4: Optional["Branch"] = None,
        fork5: Optional["Branch"] = None,
        fork6: Optional["Branch"] = None,
        fork7: Optional["Branch"] = None,
        fork8: Optional["Branch"] = None,
    ) -> "Fork":
        """The ``FORK`` processing command creates multiple execution branches to operate on the
        same input data and combines the results in a single output table.

        :param fork<n>: Up to 8 execution branches, created with the ``ESQL.branch()`` method.

        Examples::

            query = (
                ESQL.from_("employees")
                .fork(
                    ESQL.branch().where("emp_no == 10001"),
                    ESQL.branch().where("emp_no == 10002"),
                )
                .keep("emp_no", "_fork")
                .sort("emp_no")
            )
        """
        if self._is_forked():
            raise ValueError("a query can only have one fork")
        return Fork(self, fork1, fork2, fork3, fork4, fork5, fork6, fork7, fork8)

    def fuse(self, method: Optional[str] = None) -> "Fuse":
        """The ``FUSE`` processing command merges rows from multiple result sets and assigns
        new relevance scores.

        :param method: Defaults to ``RRF``. Can be one of ``RRF`` (for Reciprocal Rank Fusion)
                       or ``LINEAR`` (for linear combination of scores). Designates which
                       method to use to assign new relevance scores.

        Examples::

            query1 = (
                ESQL.from_("books").metadata("_id", "_index", "_score")
                .fork(
                    ESQL.branch().where('title:"Shakespeare"').sort("_score DESC"),
                    ESQL.branch().where('semantic_title:"Shakespeare"').sort("_score DESC"),
                )
                .fuse()
            )
            query2 = (
                ESQL.from_("books").metadata("_id", "_index", "_score")
                .fork(
                    ESQL.branch().where('title:"Shakespeare"').sort("_score DESC"),
                    ESQL.branch().where('semantic_title:"Shakespeare"').sort("_score DESC"),
                )
                .fuse("linear")
            )
            query3 = (
                ESQL.from_("books").metadata("_id", "_index", "_score")
                .fork(
                    ESQL.branch().where('title:"Shakespeare"').sort("_score DESC"),
                    ESQL.branch().where('semantic_title:"Shakespeare"').sort("_score DESC"),
                )
                .fuse("linear").by("title", "description")
            )
            query4 = (
                ESQL.from_("books").metadata("_id", "_index", "_score")
                .fork(
                    ESQL.branch().where('title:"Shakespeare"').sort("_score DESC"),
                    ESQL.branch().where('semantic_title:"Shakespeare"').sort("_score DESC"),
                )
                .fuse("linear").with_(normalizer="minmax")
            )
        """
        return Fuse(self, method)

    def grok(self, input: FieldType, pattern: str) -> "Grok":
        """``GROK`` enables you to extract structured data out of a string.

        :param input: The column that contains the string you want to structure. If the
                      column has multiple values, ``GROK`` will process each value.
        :param pattern: A grok pattern. If a field name conflicts with an existing column,
                        the existing column is discarded. If a field name is used more than
                        once, a multi-valued column will be created with one value per each
                        occurrence of the field name.

        Examples::

            query1 = (
                ESQL.row(a="2023-01-23T12:15:00.000Z 127.0.0.1 some.email@foo.com 42")
                .grok("a", "%{TIMESTAMP_ISO8601:date} %{IP:ip} %{EMAILADDRESS:email} %{NUMBER:num}")
                .keep("date", "ip", "email", "num")
            )
            query2 = (
                ESQL.row(a="2023-01-23T12:15:00.000Z 127.0.0.1 some.email@foo.com 42")
                .grok(
                    "a",
                    "%{TIMESTAMP_ISO8601:date} %{IP:ip} %{EMAILADDRESS:email} %{NUMBER:num:int}",
                )
                .keep("date", "ip", "email", "num")
                .eval(date=functions.to_datetime("date"))
            )
            query3 = (
                ESQL.from_("addresses")
                .keep("city.name", "zip_code")
                .grok("zip_code", "%{WORD:zip_parts} %{WORD:zip_parts}")
            )
        """
        return Grok(self, input, pattern)

    def inline_stats(
        self, *expressions: ExpressionType, **named_expressions: ExpressionType
    ) -> "Stats":
        """The ``INLINE STATS`` processing command groups rows according to a common value
        and calculates one or more aggregated values over the grouped rows.

        The command is identical to ``STATS`` except that it preserves all the columns from
        the input table.

        :param expressions: A list of expressions, given as positional arguments.
        :param named_expressions: A list of expressions, given as keyword arguments. The
                                  argument names are used for the returned aggregated values.

        Note that only one of ``expressions`` and ``named_expressions`` must be provided.

        Examples::

            query1 = (
                ESQL.from_("employees")
                .keep("emp_no", "languages", "salary")
                .inline_stats(max_salary=functions.max(E("salary"))).by("languages")
            )
            query2 = (
                ESQL.from_("employees")
                .keep("emp_no", "languages", "salary")
                .inline_stats(max_salary=functions.max(E("salary")))
            )
            query3 = (
                ESQL.from_("employees")
                .where("still_hired")
                .keep("emp_no", "languages", "salary", "hire_date")
                .eval(tenure=functions.date_diff("year", E("hire_date"), "2025-09-18T00:00:00"))
                .drop("hire_date")
                .inline_stats(
                    avg_salary=functions.avg(E("salary")),
                    count=functions.count(E("*")),
                )
                .by("languages", "tenure")
            )
            query4 = (
                ESQL.from_("employees")
                .keep("emp_no", "salary")
                .inline_stats(
                    avg_lt_50=functions.round(functions.avg(E("salary"))).where(E("salary") < 50000),
                    avg_lt_60=functions.round(functions.avg(E("salary"))).where(E("salary") >= 50000, E("salary") < 60000),
                    avg_gt_60=functions.round(functions.avg(E("salary"))).where(E("salary") >= 60000),
                )
            )

        """
        return InlineStats(self, *expressions, **named_expressions)

    def keep(self, *columns: FieldType) -> "Keep":
        """The ``KEEP`` processing command enables you to specify what columns are returned
        and the order in which they are returned.

        :param columns: The columns to keep, given as positional arguments. Supports
                        wildcards.

        Examples::

            query1 = ESQL.from_("employees").keep("emp_no", "first_name", "last_name", "height")
            query2 = ESQL.from_("employees").keep("h*")
            query3 = ESQL.from_("employees").keep("h*", "*")
        """
        return Keep(self, *columns)

    def limit(self, max_number_of_rows: int) -> "Limit":
        """The ``LIMIT`` processing command enables you to limit the number of rows that are
        returned.

        :param max_number_of_rows: The maximum number of rows to return.

        Examples::

            query1 = ESQL.from_("employees").sort("emp_no ASC").limit(5)
            query2 = ESQL.from_("index").stats(functions.avg("field1")).by("field2").limit(20000)
        """
        return Limit(self, max_number_of_rows)

    def lookup_join(self, lookup_index: IndexType) -> "LookupJoin":
        """``LOOKUP JOIN`` enables you to add data from another index, AKA a 'lookup' index,
        to your ES|QL query results, simplifying data enrichment and analysis workflows.

        :param lookup_index: The name of the lookup index. This must be a specific index
                             name - wildcards, aliases, and remote cluster references are
                             not supported. Indices used for lookups must be configured
                             with the lookup index mode.

        Examples::

            query1 = (
                ESQL.from_("firewall_logs")
                .lookup_join("threat_list").on("source.IP")
                .where("threat_level IS NOT NULL")
            )
            query2 = (
                ESQL.from_("system_metrics")
                .lookup_join("host_inventory").on("host.name")
                .lookup_join("ownerships").on("host.name")
            )
            query3 = (
                ESQL.from_("app_logs")
                .lookup_join("service_owners").on("service_id")
            )
            query4 = (
                ESQL.from_("employees")
                .eval(language_code="languages")
                .where("emp_no >= 10091 AND emp_no < 10094")
                .lookup_join("languages_lookup").on("language_code")
            )
        """
        return LookupJoin(self, lookup_index)

    def mv_expand(self, column: FieldType) -> "MvExpand":
        """The ``MV_EXPAND`` processing command expands multivalued columns into one row per
        value, duplicating other columns.

        :param column: The multivalued column to expand.

        Examples::

            query = ESQL.row(a=[1, 2, 3], b="b", j=["a", "b"]).mv_expand("a")
        """
        return MvExpand(self, column)

    def rename(self, **columns: FieldType) -> "Rename":
        """The ``RENAME`` processing command renames one or more columns.

        :param columns: The old and new column name pairs, given as keyword arguments.
                        If a name conflicts with an existing column name, the existing column
                        is dropped. If multiple columns are renamed to the same name, all but
                        the rightmost column with the same new name are dropped.

        Examples::

            query = (
                ESQL.from_("employees")
                .keep("first_name", "last_name", "still_hired")
                .rename(still_hired="employed")
            )
        """
        return Rename(self, **columns)

    def rerank(self, *query: ExpressionType, **named_query: ExpressionType) -> "Rerank":
        """The ``RERANK`` command uses an inference model to compute a new relevance score
        for an initial set of documents, directly within your ES|QL queries.

        :param query: The query text used to rerank the documents. This is typically the
                      same query used in the initial search.
        :param named_query: The query text used to rerank the documents, given as a
                            keyword argument. The argument name is used for the column
                            name. If the query is given as a positional argument, the
                            results will be stored in a column named ``_score``. If the
                            specified column already exists, it will be overwritten with
                            the new results.

        Examples::

            query1 = (
                ESQL.from_("books").metadata("_score")
                .where('MATCH(description, "hobbit")')
                .sort("_score DESC")
                .limit(100)
                .rerank("hobbit").on("description").with_(inference_id="test_reranker")
                .limit(3)
                .keep("title", "_score")
            )
            query2 = (
                ESQL.from_("books").metadata("_score")
                .where('MATCH(description, "hobbit") OR MATCH(author, "Tolkien")')
                .sort("_score DESC")
                .limit(100)
                .rerank(rerank_score="hobbit").on("description", "author").with_(inference_id="test_reranker")
                .sort("rerank_score")
                .limit(3)
                .keep("title", "_score", "rerank_score")
            )
            query3 = (
                ESQL.from_("books").metadata("_score")
                .where('MATCH(description, "hobbit") OR MATCH(author, "Tolkien")')
                .sort("_score DESC")
                .limit(100)
                .rerank(rerank_score="hobbit").on("description", "author").with_(inference_id="test_reranker")
                .eval(original_score="_score", _score="rerank_score + original_score")
                .sort("_score")
                .limit(3)
                .keep("title", "original_score", "rerank_score", "_score")
            )
        """
        return Rerank(self, *query, **named_query)

    def sample(self, probability: float) -> "Sample":
        """The ``SAMPLE`` command samples a fraction of the table rows.

        :param probability: The probability that a row is included in the sample. The value
                            must be between 0 and 1, exclusive.

        Examples::

            query = ESQL.from_("employees").keep("emp_no").sample(0.05)
        """
        return Sample(self, probability)

    def sort(self, *columns: ExpressionType) -> "Sort":
        """The ``SORT`` processing command sorts a table on one or more columns.

        :param columns: The columns to sort on.

        Examples::

            query1 = (
                ESQL.from_("employees")
                .keep("first_name", "last_name", "height")
                .sort("height")
            )
            query2 =  (
                ESQL.from_("employees")
                .keep("first_name", "last_name", "height")
                .sort("height DESC")
            )
            query3 = (
                ESQL.from_("employees")
                .keep("first_name", "last_name", "height")
                .sort("height DESC", "first_name ASC")
            )
            query4 = (
                ESQL.from_("employees")
                .keep("first_name", "last_name", "height")
                .sort("first_name ASC NULLS FIRST")
            )
        """
        return Sort(self, *columns)

    def stats(
        self, *expressions: ExpressionType, **named_expressions: ExpressionType
    ) -> "Stats":
        """The ``STATS`` processing command groups rows according to a common value and
        calculates one or more aggregated values over the grouped rows.

        :param expressions: A list of expressions, given as positional arguments.
        :param named_expressions: A list of expressions, given as keyword arguments. The
                                  argument names are used for the returned aggregated values.

        Note that only one of ``expressions`` and ``named_expressions`` must be provided.

        Examples::

            query1 = (
                ESQL.from_("employees")
                .stats(count=functions.count("emp_no")).by("languages")
                .sort("languages")
            )
            query2 = (
                ESQL.from_("employees")
                .stats(avg_lang=functions.avg("languages"))
            )
            query3 = (
                ESQL.from_("employees")
                .stats(
                    avg_lang=functions.avg("languages"),
                    max_lang=functions.max("languages")
                )
            )
            query4 = (
                ESQL.from_("employees")
                .stats(
                    avg50s=functions.avg("salary").where('birth_date < "1960-01-01"'),
                    avg60s=functions.avg("salary").where('birth_date >= "1960-01-01"'),
                ).by("gender")
                .sort("gender")
            )
            query5 = (
                ESQL.from_("employees")
                .eval(Ks="salary / 1000")
                .stats(
                    under_40K=functions.count("*").where("Ks < 40"),
                    inbetween=functions.count("*").where("40 <= Ks AND Ks < 60"),
                    over_60K=functions.count("*").where("60 <= Ks"),
                    total=f.count("*")
                )
            )
            query6 = (
                ESQL.row(i=1, a=["a", "b"])
                .stats(functions.min("i")).by("a")
                .sort("a ASC")
            )
            query7 = (
                ESQL.from_("employees")
                .eval(hired=functions.date_format("hire_date", "yyyy"))
                .stats(avg_salary=functions.avg("salary")).by("hired", "languages.long")
                .eval(avg_salary=functions.round("avg_salary"))
                .sort("hired", "languages.long")

            )
        """
        return Stats(self, *expressions, **named_expressions)

    def where(self, *expressions: ExpressionType) -> "Where":
        """The ``WHERE`` processing command produces a table that contains all the rows
        from the input table for which the provided condition evaluates to ``true``.

        :param expressions: A list of boolean expressions, given as positional arguments.
                            These expressions are combined with an ``AND`` logical operator.

        Examples::

            query1 = (
                ESQL.from_("employees")
                .keep("first_name", "last_name", "still_hired")
                .where("still_hired == true")
            )
            query2 = (
                ESQL.from_("sample_data")
                .where("@timestamp > NOW() - 1 hour")
            )
            query3 = (
                ESQL.from_("employees")
                .keep("first_name", "last_name", "height")
                .where("LENGTH(first_name) < 4")
            )
        """
        return Where(self, *expressions)


class From(ESQLBase):
    """Implementation of the ``FROM`` source command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    command_name = "FROM"

    def __init__(self, *indices: IndexType):
        super().__init__()
        self._indices = indices
        self._metadata_fields: Tuple[FieldType, ...] = tuple()

    def metadata(self, *fields: FieldType) -> "From":
        """Continuation of the ``FROM`` and ``TS`` source commands.

        :param fields: metadata fields to retrieve, given as positional arguments.
        """
        self._metadata_fields = fields
        return self

    def _render_internal(self) -> str:
        indices = [self._format_index(index) for index in self._indices]
        s = f'{self.command_name} {", ".join(indices)}'
        if self._metadata_fields:
            s = (
                s
                + f' METADATA {", ".join([self._format_id(field) for field in self._metadata_fields])}'
            )
        return s


class Row(ESQLBase):
    """Implementation of the ``ROW`` source command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, **params: ExpressionType):
        super().__init__()
        self._params = {
            self._format_id(k): (
                json.dumps(v)
                if not isinstance(v, InstrumentedExpression)
                else self._format_expr(v)
            )
            for k, v in params.items()
        }

    def _render_internal(self) -> str:
        return "ROW " + ", ".join([f"{k} = {v}" for k, v in self._params.items()])


class Show(ESQLBase):
    """Implementation of the ``SHOW`` source command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    which makes it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, item: str):
        super().__init__()
        self._item = item

    def _render_internal(self) -> str:
        return f"SHOW {self._format_id(self._item)}"


class TS(From):
    """Implementation of the ``TS`` source command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    command_name = "TS"


class Branch(ESQLBase):
    """Implementation of a branch inside a ``FORK`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    which makes it possible to chain all the commands that belong to the branch
    in a single expression.
    """

    def _render_internal(self) -> str:
        return ""


class ChangePoint(ESQLBase):
    """Implementation of the ``CHANGE POINT`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, value: FieldType):
        super().__init__(parent)
        self._value = value
        self._key: Optional[FieldType] = None
        self._type_name: Optional[str] = None
        self._pvalue_name: Optional[str] = None

    def on(self, key: FieldType) -> "ChangePoint":
        """Continuation of the ``CHANGE_POINT`` command.

        :param key: The column with the key to order the values by. If not specified,
                    ``@timestamp`` is used.
        """
        self._key = key
        return self

    def as_(self, type_name: str, pvalue_name: str) -> "ChangePoint":
        """Continuation of the ``CHANGE_POINT`` command.

        :param type_name: The name of the output column with the change point type.
                          If not specified, ``type`` is used.
        :param pvalue_name: The name of the output column with the p-value that indicates
                            how extreme the change point is. If not specified, ``pvalue``
                            is used.
        """
        self._type_name = type_name
        self._pvalue_name = pvalue_name
        return self

    def _render_internal(self) -> str:
        key = "" if not self._key else f" ON {self._format_id(self._key)}"
        names = (
            ""
            if not self._type_name and not self._pvalue_name
            else f' AS {self._format_id(self._type_name or "type")}, {self._format_id(self._pvalue_name or "pvalue")}'
        )
        return f"CHANGE_POINT {self._value}{key}{names}"


class Completion(ESQLBase):
    """Implementation of the ``COMPLETION`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(
        self, parent: ESQLBase, *prompt: ExpressionType, **named_prompt: ExpressionType
    ):
        if len(prompt) + len(named_prompt) > 1:
            raise ValueError(
                "this method requires either one positional or one keyword argument only"
            )
        super().__init__(parent)
        self._prompt = prompt
        self._named_prompt = named_prompt
        self._inference_id: Optional[str] = None

    def with_(self, inference_id: str) -> "Completion":
        """Continuation of the ``COMPLETION`` command.

        :param inference_id: The ID of the inference endpoint to use for the task. The
                             inference endpoint must be configured with the ``completion``
                             task type.
        """
        self._inference_id = inference_id
        return self

    def _render_internal(self) -> str:
        if self._inference_id is None:
            raise ValueError("The completion command requires an inference ID")
        with_ = {"inference_id": self._inference_id}
        if self._named_prompt:
            column = list(self._named_prompt.keys())[0]
            prompt = list(self._named_prompt.values())[0]
            return f"COMPLETION {self._format_id(column)} = {self._format_id(prompt)} WITH {json.dumps(with_)}"
        else:
            return f"COMPLETION {self._format_id(self._prompt[0])} WITH {json.dumps(with_)}"


class Dissect(ESQLBase):
    """Implementation of the ``DISSECT`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, input: FieldType, pattern: str):
        super().__init__(parent)
        self._input = input
        self._pattern = pattern
        self._separator: Optional[str] = None

    def append_separator(self, separator: str) -> "Dissect":
        """Continuation of the ``DISSECT`` command.

        :param separator: A string used as the separator between appended values,
                          when using the append modifier.
        """
        self._separator = separator
        return self

    def _render_internal(self) -> str:
        sep = (
            ""
            if self._separator is None
            else f" APPEND_SEPARATOR={json.dumps(self._separator)}"
        )
        return (
            f"DISSECT {self._format_id(self._input)} {json.dumps(self._pattern)}{sep}"
        )


class Drop(ESQLBase):
    """Implementation of the ``DROP`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, *columns: FieldType):
        super().__init__(parent)
        self._columns = columns

    def _render_internal(self) -> str:
        return f'DROP {", ".join([self._format_id(col, allow_patterns=True) for col in self._columns])}'


class Enrich(ESQLBase):
    """Implementation of the ``ENRICH`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, policy: str):
        super().__init__(parent)
        self._policy = policy
        self._match_field: Optional[FieldType] = None
        self._fields: Optional[Tuple[FieldType, ...]] = None
        self._named_fields: Optional[Dict[str, FieldType]] = None

    def on(self, match_field: FieldType) -> "Enrich":
        """Continuation of the ``ENRICH`` command.

        :param match_field: The match field. ``ENRICH`` uses its value to look for records
                            in the enrich index. If not specified, the match will be
                            performed on the column with the same name as the
                            ``match_field`` defined in the enrich policy.
        """
        self._match_field = match_field
        return self

    def with_(self, *fields: FieldType, **named_fields: FieldType) -> "Enrich":
        """Continuation of the ``ENRICH`` command.

        :param fields: The enrich fields from the enrich index that are added to the result
                       as new columns, given as positional arguments. If a column with the
                       same name as the enrich field already exists, the existing column will
                       be replaced by the new column. If not specified, each of the enrich
                       fields defined in the policy is added. A column with the same name as
                       the enrich field will be dropped unless the enrich field is renamed.
        :param named_fields: The enrich fields from the enrich index that are added to the
                             result as new columns, given as keyword arguments. The name of
                             the keyword arguments are used as column names. If a column has
                             the same name as the new name, it will be discarded. If a name
                             (new or original) occurs more than once, only the rightmost
                             duplicate creates a new column.
        """
        if fields and named_fields:
            raise ValueError(
                "this method supports positional or keyword arguments but not both"
            )
        self._fields = fields
        self._named_fields = named_fields
        return self

    def _render_internal(self) -> str:
        on = (
            ""
            if self._match_field is None
            else f" ON {self._format_id(self._match_field)}"
        )
        with_ = ""
        if self._named_fields:
            with_ = f' WITH {", ".join([f"{self._format_id(name)} = {self._format_id(field)}" for name, field in self._named_fields.items()])}'
        elif self._fields is not None:
            with_ = (
                f' WITH {", ".join([self._format_id(field) for field in self._fields])}'
            )
        return f"ENRICH {self._policy}{on}{with_}"


class Eval(ESQLBase):
    """Implementation of the ``EVAL`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(
        self,
        parent: ESQLBase,
        *columns: ExpressionType,
        **named_columns: ExpressionType,
    ):
        if columns and named_columns:
            raise ValueError(
                "this method supports positional or keyword arguments but not both"
            )
        super().__init__(parent)
        self._columns = columns or named_columns

    def _render_internal(self) -> str:
        if isinstance(self._columns, dict):
            cols = ", ".join(
                [
                    f"{self._format_id(name)} = {self._format_expr(value)}"
                    for name, value in self._columns.items()
                ]
            )
        else:
            cols = ", ".join([f"{self._format_expr(col)}" for col in self._columns])
        return f"EVAL {cols}"


class Fork(ESQLBase):
    """Implementation of the ``FORK`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(
        self,
        parent: ESQLBase,
        fork1: "Branch",
        fork2: Optional["Branch"] = None,
        fork3: Optional["Branch"] = None,
        fork4: Optional["Branch"] = None,
        fork5: Optional["Branch"] = None,
        fork6: Optional["Branch"] = None,
        fork7: Optional["Branch"] = None,
        fork8: Optional["Branch"] = None,
    ):
        super().__init__(parent)
        self._branches = [fork1, fork2, fork3, fork4, fork5, fork6, fork7, fork8]

    def _render_internal(self) -> str:
        cmds = ""
        for branch in self._branches:
            if branch:
                cmd = branch.render()[3:].replace("\n", " ")
                if cmds == "":
                    cmds = f"( {cmd} )"
                else:
                    cmds += f"\n       ( {cmd} )"
        return f"FORK {cmds}"


class Fuse(ESQLBase):
    """Implementation of the ``FUSE`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, method: Optional[str] = None):
        super().__init__(parent)
        self.method = method
        self.by_columns: List[FieldType] = []
        self.options: Dict[str, Any] = {}

    def by(self, *columns: FieldType) -> "Fuse":
        self.by_columns += list(columns)
        return self

    def with_(self, **options: Any) -> "Fuse":
        self.options = options
        return self

    def _render_internal(self) -> str:
        method = f" {self.method.upper()}" if self.method else ""
        by = (
            " " + " ".join([f"BY {column}" for column in self.by_columns])
            if self.by_columns
            else ""
        )
        with_ = " WITH " + json.dumps(self.options) if self.options else ""
        return f"FUSE{method}{by}{with_}"


class Grok(ESQLBase):
    """Implementation of the ``GROK`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, input: FieldType, pattern: str):
        super().__init__(parent)
        self._input = input
        self._pattern = pattern

    def _render_internal(self) -> str:
        return f"GROK {self._format_id(self._input)} {json.dumps(self._pattern)}"


class Keep(ESQLBase):
    """Implementation of the ``KEEP`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, *columns: FieldType):
        super().__init__(parent)
        self._columns = columns

    def _render_internal(self) -> str:
        return f'KEEP {", ".join([f"{self._format_id(col, allow_patterns=True)}" for col in self._columns])}'


class Limit(ESQLBase):
    """Implementation of the ``LIMIT`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, max_number_of_rows: int):
        super().__init__(parent)
        self._max_number_of_rows = max_number_of_rows

    def _render_internal(self) -> str:
        return f"LIMIT {json.dumps(self._max_number_of_rows)}"


class LookupJoin(ESQLBase):
    """Implementation of the ``LOOKUP JOIN`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, lookup_index: IndexType):
        super().__init__(parent)
        self._lookup_index = lookup_index
        self._field: Optional[FieldType] = None

    def on(self, field: FieldType) -> "LookupJoin":
        """Continuation of the ``LOOKUP JOIN`` command.

        :param field: The field to join on. This field must exist in both your current query
                      results and in the lookup index. If the field contains multi-valued
                      entries, those entries will not match anything (the added fields will
                      contain null for those rows).
        """
        self._field = field
        return self

    def _render_internal(self) -> str:
        if self._field is None:
            raise ValueError("Joins require a field to join on.")
        index = (
            self._lookup_index
            if isinstance(self._lookup_index, str)
            else self._lookup_index._index._name
        )
        return (
            f"LOOKUP JOIN {self._format_index(index)} ON {self._format_id(self._field)}"
        )


class MvExpand(ESQLBase):
    """Implementation of the ``MV_EXPAND`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, column: FieldType):
        super().__init__(parent)
        self._column = column

    def _render_internal(self) -> str:
        return f"MV_EXPAND {self._format_id(self._column)}"


class Rename(ESQLBase):
    """Implementation of the ``RENAME`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, **columns: FieldType):
        super().__init__(parent)
        self._columns = columns

    def _render_internal(self) -> str:
        return f'RENAME {", ".join([f"{self._format_id(old_name)} AS {self._format_id(new_name)}" for old_name, new_name in self._columns.items()])}'


class Rerank(ESQLBase):
    """Implementation of the ``RERANK`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(
        self, parent: ESQLBase, *query: ExpressionType, **named_query: ExpressionType
    ):
        if len(query) + len(named_query) > 1:
            raise ValueError(
                "this method requires either one positional or one keyword argument only"
            )
        super().__init__(parent)
        self._query = query
        self._named_query = named_query
        self._fields: Optional[Tuple[str, ...]] = None
        self._inference_id: Optional[str] = None

    def on(self, *fields: str) -> "Rerank":
        """Continuation of the ``RERANK`` command.

        :param fields: One or more fields to use for reranking. These fields should
                       contain the text that the reranking model will evaluate.
        """
        self._fields = fields
        return self

    def with_(self, inference_id: str) -> "Rerank":
        """Continuation of the ``RERANK`` command.

        :param inference_id: The ID of the inference endpoint to use for the task. The
                             inference endpoint must be configured with the ``rerank``
                             task type.
        """
        self._inference_id = inference_id
        return self

    def _render_internal(self) -> str:
        if self._fields is None:
            raise ValueError(
                "The rerank command requires one or more fields to rerank on"
            )
        if self._inference_id is None:
            raise ValueError("The completion command requires an inference ID")
        with_ = {"inference_id": self._inference_id}
        if self._named_query:
            column = list(self._named_query.keys())[0]
            query = list(self._named_query.values())[0]
            query = f"{self._format_id(column)} = {json.dumps(query)}"
        else:
            query = json.dumps(self._query[0])
        return (
            f"RERANK {query} "
            f"ON {', '.join([self._format_id(field) for field in self._fields])} "
            f"WITH {json.dumps(with_)}"
        )


class Sample(ESQLBase):
    """Implementation of the ``SAMPLE`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, probability: float):
        super().__init__(parent)
        self._probability = probability

    def _render_internal(self) -> str:
        return f"SAMPLE {json.dumps(self._probability)}"


class Sort(ESQLBase):
    """Implementation of the ``SORT`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, *columns: ExpressionType):
        super().__init__(parent)
        self._columns = columns

    def _render_internal(self) -> str:
        sorts = [
            " ".join([self._format_id(term) for term in str(col).split(" ")])
            for col in self._columns
        ]
        return f'SORT {", ".join([f"{sort}" for sort in sorts])}'


class Stats(ESQLBase):
    """Implementation of the ``STATS`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    command_name = "STATS"

    def __init__(
        self,
        parent: ESQLBase,
        *expressions: ExpressionType,
        **named_expressions: ExpressionType,
    ):
        if expressions and named_expressions:
            raise ValueError(
                "this method supports positional or keyword arguments but not both"
            )
        super().__init__(parent)
        self._expressions = expressions or named_expressions
        self._grouping_expressions: Optional[Tuple[ExpressionType, ...]] = None

    def by(self, *grouping_expressions: ExpressionType) -> "Stats":
        """Continuation of the ``STATS`` and ``INLINE STATS`` commands.

        :param grouping_expressions: Expressions that output the values to group by.
                                     If their names coincide with one of the computed
                                     columns, that column will be ignored.
        """
        self._grouping_expressions = grouping_expressions
        return self

    def _render_internal(self) -> str:
        if isinstance(self._expressions, dict):
            exprs = [
                f"{self._format_id(key)} = {self._format_expr(value)}"
                for key, value in self._expressions.items()
            ]
        else:
            exprs = [f"{self._format_expr(expr)}" for expr in self._expressions]
        indent = " " * (len(self.command_name) + 3)
        expression_separator = f",\n{indent}"
        by = (
            ""
            if self._grouping_expressions is None
            else f'\n{indent}BY {", ".join([f"{self._format_expr(expr)}" for expr in self._grouping_expressions])}'
        )
        return f'{self.command_name} {expression_separator.join([f"{expr}" for expr in exprs])}{by}'


class InlineStats(Stats):
    """Implementation of the ``INLINE STATS`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    command_name = "INLINE STATS"


class Where(ESQLBase):
    """Implementation of the ``WHERE`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, *expressions: ExpressionType):
        super().__init__(parent)
        self._expressions = expressions

    def _render_internal(self) -> str:
        return f'WHERE {" AND ".join([f"{self._format_expr(expr)}" for expr in self._expressions])}'


def and_(*expressions: InstrumentedExpression) -> "InstrumentedExpression":
    """Combine two or more expressions with the AND operator."""
    return InstrumentedExpression(" AND ".join([f"({expr})" for expr in expressions]))


def or_(*expressions: InstrumentedExpression) -> "InstrumentedExpression":
    """Combine two or more expressions with the OR operator."""
    return InstrumentedExpression(" OR ".join([f"({expr})" for expr in expressions]))


def not_(expression: InstrumentedExpression) -> "InstrumentedExpression":
    """Negate an expression."""
    return InstrumentedExpression(f"NOT ({expression})")
