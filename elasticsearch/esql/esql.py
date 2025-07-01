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
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple, Type

from ..dsl.document_base import DocumentBase, InstrumentedField

FieldType = InstrumentedField | str
IndexType = Type[DocumentBase] | str
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

            ESQL.from_("employees")
            ESQL.from_("<logs-{now/d}>")
            ESQL.from_("employees-00001", "other-employees-*")
            ESQL.from_("cluster_one:employees-00001", "cluster_two:other-employees-*")
            ESQL.from_("employees").metadata("_id")
        """
        return From(*indices)

    @staticmethod
    def row(**params: ExpressionType) -> "Row":
        """The ``ROW`` source command produces a row with one or more columns with values that you specify.
        This can be useful for testing.

        :param params: the column values to produce, given as keyword arguments.

        Examples::

            ESQL.row(a=1, b="two", c=None)
            ESQL.row(a=[1, 2])
            ESQL.row(a="ROUND(1.23, 0)")
        """
        return Row(**params)

    @staticmethod
    def show(item: str) -> "Show":
        """The ``SHOW`` source command returns information about the deployment and its capabilities.

        :param item: Can only be ``INFO``.

        Examples::

            ESQL.show("INFO")
        """
        return Show(item)


class ESQLBase(ABC):
    """ """

    def __init__(self, parent: Optional["ESQLBase"] = None):
        self.parent = parent

    def __repr__(self) -> str:
        return self.render()

    def render(self) -> str:
        return (
            self.parent.render() + "\n| " if self.parent else ""
        ) + self._render_internal()

    @abstractmethod
    def _render_internal(self) -> str:
        pass

    # def change_point(self, value: FieldType) -> "ChangePoint":
    #     """`CHANGE_POINT` detects spikes, dips, and change points in a metric.
    #
    #     :param value: The column with the metric in which you want to detect a change point.
    #
    #     Examples::
    #
    #         (
    #             ESQL.row(key=list(range(1, 26)))
    #             .mv_expand("key")
    #             .eval(value="CASE(key<13, 0, 42)")
    #             .change_point("value").on("key")
    #             .where("type IS NOT NULL")
    #         )
    #     """
    #     return ChangePoint(self, value)

    def dissect(self, input: FieldType, pattern: str) -> "Dissect":
        """``DISSECT`` enables you to extract structured data out of a string.

        :param input: The column that contains the string you want to structure. If
                      the column has multiple values, ``DISSECT`` will process each value.
        :param pattern: A dissect pattern. If a field name conflicts with an existing
                        column, the existing column is dropped. If a field name is used
                        more than once, only the rightmost duplicate creates a column.

        Examples::

            (
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

            ESQL.from_("employees").drop("height")
            ESQL.from_("employees").drop("height*")
        """
        return Drop(self, *columns)

    def enrich(self, policy: str) -> "Enrich":
        """``ENRICH`` enables you to add data from existing indices as new columns using an
        enrich policy.

        :param policy: The name of the enrich policy. You need to create and execute the
                       enrich policy first.

        Examples::

            (
                ESQL.row(a="1")
                .enrich("languages_policy").on("a").with_("language_name")
            )
            (
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

            (
                ESQL.from_("employees")
                .sort("emp_no")
                .keep("first_name", "last_name", "height")
                .eval(height_feet="height * 3.281", height_cm="height * 100")
            )
            (
                ESQL.from_("employees")
                .eval("height * 3.281")
                .stats(avg_height_feet="AVG(`height * 3.281`)")
            )
        """
        return Eval(self, *columns, **named_columns)

    def grok(self, input: FieldType, pattern: str) -> "Grok":
        """``GROK`` enables you to extract structured data out of a string.

        :param input: The column that contains the string you want to structure. If the
                      column has multiple values, ``GROK`` will process each value.
        :param pattern: A grok pattern. If a field name conflicts with an existing column,
                        the existing column is discarded. If a field name is used more than
                        once, a multi-valued column will be created with one value per each
                        occurrence of the field name.

        Examples::

            (
                ESQL.row(a="2023-01-23T12:15:00.000Z 127.0.0.1 some.email@foo.com 42")
                .grok("a", "%{TIMESTAMP_ISO8601:date} %{IP:ip} %{EMAILADDRESS:email} %{NUMBER:num}")
                .keep("date", "ip", "email", "num")
            )
            (
                ESQL.from_("addresses")
                .keep("city.name", "zip_code")
                .grok("zip_code", "%{WORD:zip_parts} %{WORD:zip_parts}")
            )
        """
        return Grok(self, input, pattern)

    def keep(self, *columns: FieldType) -> "Keep":
        """The ``KEEP`` processing command enables you to specify what columns are returned
        and the order in which they are returned.

        :param columns: The columns to keep, given as positional arguments. Supports
                        wildcards.

        Examples::

            ESQL.from_("employees").keep("emp_no", "first_name", "last_name", "height")
            ESQL.from_("employees").keep("h*")
            ESQL.from_("employees").keep("h*", "*")
        """
        return Keep(self, *columns)

    def limit(self, max_number_of_rows: int) -> "Limit":
        """The ``LIMIT`` processing command enables you to limit the number of rows that are
        returned.

        :param max_number_of_rows: The maximum number of rows to return.

        Examples::

            ESQL.from_("employees").sort("emp_no ASC").limit(5)
        """
        return Limit(self, max_number_of_rows)

    def lookup_join(self, lookup_index: IndexType, field: FieldType) -> "LookupJoin":
        """`LOOKUP JOIN` enables you to add data from another index, AKA a 'lookup' index,
        to your ES|QL query results, simplifying data enrichment and analysis workflows.

        :param lookup_index: The name of the lookup index. This must be a specific index
                             name - wildcards, aliases, and remote cluster references are
                             not supported. Indices used for lookups must be configured
                             with the lookup index mode.
        :param field: The field to join on. This field must exist in both your current query
                      results and in the lookup index. If the field contains multi-valued
                      entries, those entries will not match anything (the added fields will
                      contain null for those rows).

        Examples::

            (
                ESQL.from_("firewall_logs")
                .lookup_join("threat_list").on("source.IP")
                .where("threat_level IS NOT NULL")
            )
            (
                ESQL.from_("system_metrics")
                .lookup_join("host_inventory").on("host.name")
                .lookup_join("ownerships").on("host.name")
            )
            (
                ESQL.from_("app_logs")
                .lookup_join("service_owners").on("service_id")
            )
            (
                ESQL.from_("employees")
                .eval(language_code="languages")
                .where("emp_no >= 10991 AND emp_no < 10094")
                .lookup_join("languages_lookup").on("language_code")
            )
        """
        return LookupJoin(self, lookup_index, field)

    def mv_expand(self, column: FieldType) -> "MvExpand":
        """The `MV_EXPAND` processing command expands multivalued columns into one row per
        value, duplicating other columns.

        :param column: The multivalued column to expand.

        Examples::

            ESQL.row(a=[1, 2, 3], b="b", j=["a", "b"]).mv_expand("a")
        """
        return MvExpand(self, column)

    def rename(self, **columns: FieldType) -> "Rename":
        """The ``RENAME`` processing command renames one or more columns.

        :param columns: The old and new column name pairs, given as keyword arguments.
                        If a name conflicts with an existing column name, the existing column
                        is dropped. If multiple columns are renamed to the same name, all but
                        the rightmost column with the same new name are dropped.

        Examples::

            (
                ESQL.from_("employees")
                .keep("first_name", "last_name", "height")
                .rename(still_hired="employed")
            )
        """
        return Rename(self, **columns)

    def sample(self, probability: float) -> "Sample":
        """The ``SAMPLE`` command samples a fraction of the table rows.

        :param probability: The probability that a row is included in the sample. The value
                            must be between 0 and 1, exclusive.

        Examples::

            ESQL.from_("employees").keep("emp_no").sample(0.05)
        """
        return Sample(self, probability)

    def sort(self, *columns: FieldType) -> "Sort":
        """The ``SORT`` processing command sorts a table on one or more columns.

        :param columns: The columns to sort on.

        Examples::

            (
                ESQL.from_("employees")
                .keep("first_name", "last_name", "height")
                .sort("height")
            )
            (
                ESQL.from_("employees")
                .keep("first_name", "last_name", "height")
                .sort("height DESC")
            )
            (
                ESQL.from_("employees")
                .keep("first_name", "last_name", "height")
                .sort("height DESC", "first_name ASC")
            )
            (
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

        Note that only one of `expressions` and `named_expressions` must be provided.

        Examples::

            (
                ESQL.from_("employees")
                .stats(count="COUNT(emp_no)").by("languages")
                .sort("languages")
            )
            (
                ESQL.from_("employees")
                .stats(avg_lang="AVG(languages)")
                .sort("languages")
            )
            (
                ESQL.from_("employees")
                .stats(avg_lang="AVG(languages)", max_lang="MAX(languages)")
            )
            (
                ESQL.from_("employees")
                .stats(
                    avg50s='AVG(salary)::LONG WHERE birth_date < "1960-01-01"',
                    avg60s='AVG(salary)::LONG WHERE birth_date >= "1960-01-01"',
                ).by("gender")
                .sort("gender")
            )
            (
                ESQL.from_("employees")
                .stats(
                    under_40K="COUNT(*) WHERE Ks < 40",
                    inbetween="COUNT(*) WHERE 50 <= Ks AND Ks < 60",
                    over_60K="COUNT(*) WHERE 60 <= Ks",
                    total=COUNT(*)
                )
            )
            (
                ESQL.row(i=1, a=["a", "b"])
                .stats("MIN(i)").by("a")
                .sort("a ASC")
            )
            (
                ESQL.from_("employees")
                .eval(hired='DATE_FORMAT("yyyy", hire_date)')
                .stats(avg_salary="AVG(salary)").by("hired", "languages.long")
                .eval(avg_salary="ROUND(avg_salary)")
                .sort("hired", "languages.long")
            )
        """
        return Stats(self, *expressions, **named_expressions)

    def where(self, *expressions: ExpressionType) -> "Where":
        """The ``WHERE`` processing command produces a table that contains all the rows
        from the input table for which the provided condition evaluates to `true`.

        :param expressions: A list of boolean expressions, given as positional arguments.
                            These expressions are combined with an ``AND`` logical operator.

        Examples::

            (
                ESQL.from_("employees")
                .keep("first_name", "last_name", "still_hired")
                .where("still_hired == true")
            )
            (
                ESQL.from_("sample_data")
                .where("@timestamp > NOW() - 1 hour")
            )
            (
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

    def __init__(self, *indices: IndexType):
        super().__init__()
        self._indices = indices
        self._metadata_fields: Tuple[FieldType, ...] = tuple()

    def metadata(self, *fields: FieldType) -> "From":
        """Continuation of the ``FROM`` source command.

        :param fields: metadata fields to retrieve, given as positional arguments.
        """
        self._metadata_fields = fields
        return self

    def _render_internal(self) -> str:
        indices = [
            index if isinstance(index, str) else index._index._name
            for index in self._indices
        ]
        s = f'{self.__class__.__name__.upper()} {", ".join(indices)}'
        if self._metadata_fields:
            s = (
                s
                + f' METADATA {", ".join([str(field) for field in self._metadata_fields])}'
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
        self._params = params

    def _render_internal(self) -> str:
        return "ROW " + ", ".join(
            [f"{k} = {json.dumps(v)}" for k, v in self._params.items()]
        )


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
        return f"SHOW {self._item}"


# class ChangePoint(ESQLBase):
#     """Implementation of the ``CHANGE POINT`` processing command.
#
#     This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
#     to make it possible to chain all the commands that belong to an ES|QL query
#     in a single expression.
#     """
#     def __init__(self, parent: ESQLBase, value: FieldType):
#         super().__init__(parent)
#         self._value = value
#         self._key: Optional[FieldType] = None
#         self._type_name: Optional[str] = None
#         self._pvalue_name: Optional[str] = None
#
#     def on(self, key: FieldType) -> "ChangePoint":
#         """Continuation of the `CHANGE_POINT` command.
#
#         :param key: The column with the key to order the values by. If not specified,
#                     `@timestamp` is used.
#         """
#         self._key = key
#         return self
#
#     def as_(self, type_name: str, pvalue_name: str) -> "ChangePoint":
#         """Continuation of the `CHANGE_POINT` command.
#
#         :param type_name: The name of the output column with the change point type.
#                           If not specified, `type` is used.
#         :param pvalue_name: The name of the output column with the p-value that indicates
#                             how extreme the change point is. If not specified, `pvalue` is used.
#         """
#         self._type_name = type_name
#         self._pvalue_name = pvalue_name
#         return self
#
#     def _render_internal(self) -> str:
#         key = "" if not self._key else f" ON {self._key}"
#         names = (
#             ""
#             if not self._type_name and not self._pvalue_name
#             else f' AS {self._type_name or "type"}, {self._pvalue_name or "pvalue"}'
#         )
#         return f"CHANGE_POINT {self._value}{key}{names}"


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
            "" if self._separator is None else f' APPEND_SEPARATOR="{self._separator}"'
        )
        return f"DISSECT {self._input} {json.dumps(self._pattern)}{sep}"


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
        return f'DROP {", ".join([str(col) for col in self._columns])}'


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
                            `match_field` defined in the enrich policy.
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
        on = "" if self._match_field is None else f" ON {self._match_field}"
        with_ = ""
        if self._named_fields:
            with_ = f' WITH {", ".join([f"{name} = {field}" for name, field in self._named_fields.items()])}'
        elif self._fields is not None:
            with_ = f' WITH {", ".join([str(field) for field in self._fields])}'
        return f"ENRICH {self._policy}{on}{with_}"


class Eval(ESQLBase):
    """Implementation of the ``EVAL`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(
        self, parent: ESQLBase, *columns: FieldType, **named_columns: FieldType
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
                [f"{name} = {value}" for name, value in self._columns.items()]
            )
        else:
            cols = ", ".join([f"{col}" for col in self._columns])
        return f"EVAL {cols}"


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
        return f"GROK {self._input} {json.dumps(self._pattern)}"


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
        return f'KEEP {", ".join([f"{col}" for col in self._columns])}'


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
        return f"LIMIT {self._max_number_of_rows}"


class LookupJoin(ESQLBase):
    """Implementation of the ``LOOKUP JOIN`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, lookup_index: IndexType, field: FieldType):
        super().__init__(parent)
        self._lookup_index = lookup_index
        self._field = field

    def _render_internal(self) -> str:
        index = (
            self._lookup_index
            if isinstance(self._lookup_index, str)
            else self._lookup_index._index._name
        )
        return f"LOOKUP JOIN {index} ON {self._field}"


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
        return f"MV_EXPAND {self._column}"


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
        return f'RENAME {", ".join([f"{old_name} AS {new_name}" for old_name, new_name in self._columns.items()])}'


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
        return f"SAMPLE {self._probability}"


class Sort(ESQLBase):
    """Implementation of the ``SORT`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

    def __init__(self, parent: ESQLBase, *columns: FieldType):
        super().__init__(parent)
        self._columns = columns

    def _render_internal(self) -> str:
        return f'SORT {", ".join([f"{col}" for col in self._columns])}'


class Stats(ESQLBase):
    """Implementation of the ``STATS`` processing command.

    This class inherits from :class:`ESQLBase <elasticsearch.esql.esql.ESQLBase>`,
    to make it possible to chain all the commands that belong to an ES|QL query
    in a single expression.
    """

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
        self._grouping_expressions = grouping_expressions
        return self

    def _render_internal(self) -> str:
        if isinstance(self._expressions, dict):
            exprs = [f"{key} = {value}" for key, value in self._expressions.items()]
        else:
            exprs = [f"{expr}" for expr in self._expressions]
        by = (
            ""
            if self._grouping_expressions is None
            else f'BY {", ".join([f"{expr}" for expr in self._grouping_expressions])}'
        )
        return f'STATS {", ".join([f"{expr}" for expr in exprs])}{by}'


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
        return f'WHERE {" AND ".join([f"{expr}" for expr in self._expressions])}'
