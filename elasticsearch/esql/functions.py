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

from elasticsearch.dsl.document_base import InstrumentedExpression
from elasticsearch.esql.esql import ExpressionType


def abs(number: ExpressionType) -> InstrumentedExpression:
    """Returns the absolute value.

    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ABS({number})")


def acos(number: ExpressionType) -> InstrumentedExpression:
    """Returns the arccosine of `n` as an angle, expressed in radians.

    :arg number: Number between -1 and 1. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ACOS({number})")


def asin(number: ExpressionType) -> InstrumentedExpression:
    """Returns the arcsine of the input numeric expression as an angle,
    expressed in radians.

    :arg number: Number between -1 and 1. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ASIN({number})")


def atan(number: ExpressionType) -> InstrumentedExpression:
    """Returns the arctangent of the input numeric expression as an angle,
    expressed in radians.

    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ATAN({number})")


def atan2(
    y_coordinate: ExpressionType, x_coordinate: ExpressionType
) -> InstrumentedExpression:
    """The angle between the positive x-axis and the ray from the origin to the
    point (x , y) in the Cartesian plane, expressed in radians.

    :arg y_coordinate: y coordinate. If `null`, the function returns `null`.
    :arg x_coordinate: x coordinate. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ATAN2({y_coordinate}, {x_coordinate})")


def avg(number: ExpressionType) -> InstrumentedExpression:
    """The average of a numeric field.

    :arg number: Expression that outputs values to average.
    """
    return InstrumentedExpression(f"AVG({number})")


def avg_over_time(number: ExpressionType) -> InstrumentedExpression:
    """The average over time of a numeric field.

    :arg number: Expression that outputs values to average.
    """
    return InstrumentedExpression(f"AVG_OVER_TIME({number})")


def bit_length(string: ExpressionType) -> InstrumentedExpression:
    """Returns the bit length of a string.

    :arg string: String expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"BIT_LENGTH({string})")


def bucket(
    field: ExpressionType,
    buckets: ExpressionType,
    from_: ExpressionType,
    to: ExpressionType,
) -> InstrumentedExpression:
    """Creates groups of values - buckets - out of a datetime or numeric input.
    The size of the buckets can either be provided directly, or chosen based on
    a recommended count and values range.

    :arg field: Numeric or date expression from which to derive buckets.
    :arg buckets: Target number of buckets, or desired bucket size if `from`
    and `to` parameters are omitted.
    :arg from_: Start of the range. Can be a number, a date or a date expressed
    as a string.
    :arg to: End of the range. Can be a number, a date or a date expressed as a string.
    """
    return InstrumentedExpression(f"BUCKET({field}, {buckets}, {from_}, {to})")


def byte_length(string: ExpressionType) -> InstrumentedExpression:
    """Returns the byte length of a string.

    :arg string: String expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"BYTE_LENGTH({string})")


def case(*conditions: ExpressionType) -> InstrumentedExpression:
    """Accepts pairs of conditions and values. The function returns the value
    that belongs to the first condition that evaluates to `true`.  If the
    number of arguments is odd, the last argument is the default value which is
    returned when no condition matches. If the number of arguments is even, and
    no condition matches, the function returns `null`.

    :arg condition: A condition.
    :arg true_value: The value that’s returned when the corresponding condition
    is the first to evaluate to `true`. The default value is returned when no
    condition matches.
    :arg else_value: The value that’s returned when no condition evaluates to `true`.
    """
    return InstrumentedExpression(f'CASE({", ".join([str(c) for c in conditions])})')


def categorize(field: ExpressionType) -> InstrumentedExpression:
    """Groups text messages into categories of similarly formatted text values.

    :arg field: Expression to categorize
    """
    return InstrumentedExpression(f"CATEGORIZE({field})")


def cbrt(number: ExpressionType) -> InstrumentedExpression:
    """Returns the cube root of a number. The input can be any numeric value,
    the return value is always a double. Cube roots of infinities are null.

    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"CBRT({number})")


def ceil(number: ExpressionType) -> InstrumentedExpression:
    """Round a number up to the nearest integer.

    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"CEIL({number})")


def cidr_match(ip: ExpressionType, block_x: ExpressionType) -> InstrumentedExpression:
    """Returns true if the provided IP is contained in one of the provided CIDR blocks.

    :arg ip: IP address of type `ip` (both IPv4 and IPv6 are supported).
    :arg block_x: CIDR block to test the IP against.
    """
    return InstrumentedExpression(f"CIDR_MATCH({ip}, {block_x})")


def coalesce(first: ExpressionType, rest: ExpressionType) -> InstrumentedExpression:
    """Returns the first of its arguments that is not null. If all arguments
    are null, it returns `null`.

    :arg first: Expression to evaluate.
    :arg rest: Other expression to evaluate.
    """
    return InstrumentedExpression(f"COALESCE({first}, {rest})")


def concat(string1: ExpressionType, string2: ExpressionType) -> InstrumentedExpression:
    """Concatenates two or more strings.

    :arg string1: Strings to concatenate.
    :arg string2: Strings to concatenate.
    """
    return InstrumentedExpression(f"CONCAT({string1}, {string2})")


def cos(angle: ExpressionType) -> InstrumentedExpression:
    """Returns the cosine of an angle.

    :arg angle: An angle, in radians. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"COS({angle})")


def cosh(number: ExpressionType) -> InstrumentedExpression:
    """Returns the hyperbolic cosine of a number.

    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"COSH({number})")


def count(field: ExpressionType) -> InstrumentedExpression:
    """Returns the total number (count) of input values.

    :arg field: Expression that outputs values to be counted. If omitted,
    equivalent to `COUNT(*)` (the number of rows).
    """
    return InstrumentedExpression(f"COUNT({field})")


def count_distinct(
    field: ExpressionType, precision: ExpressionType
) -> InstrumentedExpression:
    """Returns the approximate number of distinct values.

    :arg field: Column or literal for which to count the number of distinct values.
    :arg precision: Precision threshold. Refer to
    [`AGG-COUNT-DISTINCT-APPROXIMATE`](/reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-agg-count-distinct-approximate).
    The maximum supported value is 40000. Thresholds above this number will
    have the same effect as a threshold of 40000. The default value is 3000.
    """
    return InstrumentedExpression(f"COUNT_DISTINCT({field}, {precision})")


def count_distinct_over_time(
    field: ExpressionType, precision: ExpressionType
) -> InstrumentedExpression:
    """The count of distinct values over time for a field.

    :arg field:
    :arg precision: Precision threshold. Refer to
    [`AGG-COUNT-DISTINCT-APPROXIMATE`](/reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-agg-count-distinct-approximate).
    The maximum supported value is 40000. Thresholds above this number will
    have the same effect as a threshold of 40000. The default value is 3000.
    """
    return InstrumentedExpression(f"COUNT_DISTINCT_OVER_TIME({field}, {precision})")


def count_over_time(field: ExpressionType) -> InstrumentedExpression:
    """The count over time value of a field.

    :arg field:
    """
    return InstrumentedExpression(f"COUNT_OVER_TIME({field})")


def date_diff(
    unit: ExpressionType, start_timestamp: ExpressionType, end_timestamp: ExpressionType
) -> InstrumentedExpression:
    """Subtracts the `startTimestamp` from the `endTimestamp` and returns the
    difference in multiples of `unit`. If `startTimestamp` is later than the
    `endTimestamp`, negative values are returned.

    :arg unit: Time difference unit
    :arg start_timestamp: A string representing a start timestamp
    :arg end_timestamp: A string representing an end timestamp
    """
    return InstrumentedExpression(
        f"DATE_DIFF({unit}, {start_timestamp}, {end_timestamp})"
    )


def date_extract(
    date_part: ExpressionType, date: ExpressionType
) -> InstrumentedExpression:
    """Extracts parts of a date, like year, month, day, hour.

    :arg date_part: Part of the date to extract.  Can be:
    `aligned_day_of_week_in_month`, `aligned_day_of_week_in_year`,
    `aligned_week_of_month`, `aligned_week_of_year`, `ampm_of_day`,
    `clock_hour_of_ampm`, `clock_hour_of_day`, `day_of_month`, `day_of_week`,
    `day_of_year`, `epoch_day`, `era`, `hour_of_ampm`, `hour_of_day`,
    `instant_seconds`, `micro_of_day`, `micro_of_second`, `milli_of_day`,
    `milli_of_second`, `minute_of_day`, `minute_of_hour`, `month_of_year`,
    `nano_of_day`, `nano_of_second`, `offset_seconds`, `proleptic_month`,
    `second_of_day`, `second_of_minute`, `year`, or `year_of_era`. Refer to
    [java.time.temporal.ChronoField](https://docs.oracle.com/javase/8/docs/api/java/time/temporal/ChronoField.html)
    for a description of these values.  If `null`, the function returns `null`.
    :arg date: Date expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"DATE_EXTRACT({date_part}, {date})")


def date_format(
    date: ExpressionType,
    date_format: ExpressionType = None,
) -> InstrumentedExpression:
    """Returns a string representation of a date, in the provided format.

    :arg date_format: Date format (optional).  If no format is specified, the
    `yyyy-MM-dd'T'HH:mm:ss.SSSZ` format is used. If `null`, the function
    returns `null`.
    :arg date: Date expression. If `null`, the function returns `null`.
    """
    if date_format is not None:
        return InstrumentedExpression(f"DATE_FORMAT({json.dumps(date_format)}, {date})")
    else:
        return InstrumentedExpression(f"DATE_FORMAT({date})")


def date_parse(
    date_pattern: ExpressionType, date_string: ExpressionType
) -> InstrumentedExpression:
    """Returns a date by parsing the second argument using the format specified
    in the first argument.

    :arg date_pattern: The date format. Refer to the [`DateTimeFormatter`
    documentation](https://docs.oracle.com/en/java/javase/14/docs/api/java.base/java/time/format/DateTimeFormatter.html)
    for the syntax. If `null`, the function returns `null`.
    :arg date_string: Date expression as a string. If `null` or an empty
    string, the function returns `null`.
    """
    return InstrumentedExpression(f"DATE_PARSE({date_pattern}, {date_string})")


def date_trunc(
    interval: ExpressionType, date: ExpressionType
) -> InstrumentedExpression:
    """Rounds down a date to the closest interval since epoch, which starts at `0001-01-01T00:00:00Z`.

    :arg interval: Interval; expressed using the timespan literal syntax.
    :arg date: Date expression
    """
    return InstrumentedExpression(f"DATE_TRUNC({interval}, {date})")


def e() -> InstrumentedExpression:
    """Returns Euler’s number)."""
    return InstrumentedExpression("E()")


def ends_with(str: ExpressionType, suffix: ExpressionType) -> InstrumentedExpression:
    """Returns a boolean that indicates whether a keyword string ends with
    another string.

    :arg str: String expression. If `null`, the function returns `null`.
    :arg suffix: String expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ENDS_WITH({str}, {suffix})")


def exp(number: ExpressionType) -> InstrumentedExpression:
    """Returns the value of e raised to the power of the given number.

    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"EXP({number})")


def first_over_time(field: ExpressionType) -> InstrumentedExpression:
    """The earliest value of a field, where recency determined by the
    `@timestamp` field.

    :arg field:
    """
    return InstrumentedExpression(f"FIRST_OVER_TIME({field})")


def floor(number: ExpressionType) -> InstrumentedExpression:
    """Round a number down to the nearest integer.

    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"FLOOR({number})")


def from_base64(string: ExpressionType) -> InstrumentedExpression:
    """Decode a base64 string.

    :arg string: A base64 string.
    """
    return InstrumentedExpression(f"FROM_BASE64({string})")


def greatest(first: ExpressionType, rest: ExpressionType) -> InstrumentedExpression:
    """Returns the maximum value from multiple columns. This is similar to
    `MV_MAX` except it is intended to run on multiple columns at once.

    :arg first: First of the columns to evaluate.
    :arg rest: The rest of the columns to evaluate.
    """
    return InstrumentedExpression(f"GREATEST({first}, {rest})")


def hash(algorithm: ExpressionType, input: ExpressionType) -> InstrumentedExpression:
    """Computes the hash of the input using various algorithms such as MD5,
    SHA, SHA-224, SHA-256, SHA-384, SHA-512.

    :arg algorithm: Hash algorithm to use.
    :arg input: Input to hash.
    """
    return InstrumentedExpression(f"HASH({algorithm}, {input})")


def hypot(number1: ExpressionType, number2: ExpressionType) -> InstrumentedExpression:
    """Returns the hypotenuse of two numbers. The input can be any numeric
    values, the return value is always a double. Hypotenuses of infinities are null.

    :arg number1: Numeric expression. If `null`, the function returns `null`.
    :arg number2: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"HYPOT({number1}, {number2})")


def ip_prefix(
    ip: ExpressionType,
    prefix_length_v4: ExpressionType,
    prefix_length_v6: ExpressionType,
) -> InstrumentedExpression:
    """Truncates an IP to a given prefix length.

    :arg ip: IP address of type `ip` (both IPv4 and IPv6 are supported).
    :arg prefix_length_v4: Prefix length for IPv4 addresses.
    :arg prefix_length_v6: Prefix length for IPv6 addresses.
    """
    return InstrumentedExpression(
        f"IP_PREFIX({ip}, {prefix_length_v4}, {prefix_length_v6})"
    )


def knn(
    field: ExpressionType, query: ExpressionType, options: ExpressionType = None
) -> InstrumentedExpression:
    """Finds the k nearest vectors to a query vector, as measured by a
    similarity metric. knn function finds nearest vectors through approximate
    search on indexed dense_vectors.

    :arg field: Field that the query will target.
    :arg query: Vector value to find top nearest neighbours for.
    :arg options: (Optional) kNN additional options as function named parameters.
    """
    if options is not None:
        return InstrumentedExpression(f"KNN({field}, {query}, {options})")
    else:
        return InstrumentedExpression(f"KNN({field}, {query})")


def kql(query: ExpressionType) -> InstrumentedExpression:
    """Performs a KQL query. Returns true if the provided KQL query string
    matches the row.

    :arg query: Query string in KQL query string format.
    """
    return InstrumentedExpression(f"KQL({query})")


def last_over_time(field: ExpressionType) -> InstrumentedExpression:
    """The latest value of a field, where recency determined by the
    `@timestamp` field.

    :arg field:
    """
    return InstrumentedExpression(f"LAST_OVER_TIME({field})")


def least(first: ExpressionType, rest: ExpressionType) -> InstrumentedExpression:
    """Returns the minimum value from multiple columns. This is similar to
    `MV_MIN` except it is intended to run on multiple columns at once.

    :arg first: First of the columns to evaluate.
    :arg rest: The rest of the columns to evaluate.
    """
    return InstrumentedExpression(f"LEAST({first}, {rest})")


def left(string: ExpressionType, length: ExpressionType) -> InstrumentedExpression:
    """Returns the substring that extracts *length* chars from *string*
    starting from the left.

    :arg string: The string from which to return a substring.
    :arg length: The number of characters to return.
    """
    return InstrumentedExpression(f"LEFT({string}, {length})")


def length(string: ExpressionType) -> InstrumentedExpression:
    """Returns the character length of a string.

    :arg string: String expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"LENGTH({string})")


def locate(
    string: ExpressionType, substring: ExpressionType, start: ExpressionType
) -> InstrumentedExpression:
    """Returns an integer that indicates the position of a keyword substring
    within another string. Returns `0` if the substring cannot be found. Note
    that string positions start from `1`.

    :arg string: An input string
    :arg substring: A substring to locate in the input string
    :arg start: The start index
    """
    return InstrumentedExpression(f"LOCATE({string}, {substring}, {start})")


def log(base: ExpressionType, number: ExpressionType) -> InstrumentedExpression:
    """Returns the logarithm of a value to a base. The input can be any numeric
    value, the return value is always a double.  Logs of zero, negative
    numbers, and base of one return `null` as well as a warning.

    :arg base: Base of logarithm. If `null`, the function returns `null`. If
    not provided, this function returns the natural logarithm (base e) of a value.
    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"LOG({base}, {number})")


def log10(number: ExpressionType) -> InstrumentedExpression:
    """Returns the logarithm of a value to base 10. The input can be any
    numeric value, the return value is always a double.  Logs of 0 and negative
    numbers return `null` as well as a warning.

    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"LOG10({number})")


def ltrim(string: ExpressionType) -> InstrumentedExpression:
    """Removes leading whitespaces from a string.

    :arg string: String expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"LTRIM({string})")


def match(
    field: ExpressionType, query: ExpressionType, options: ExpressionType = None
) -> InstrumentedExpression:
    """Use `MATCH` to perform a match query on the specified field. Using
    `MATCH` is equivalent to using the `match` query in the Elasticsearch Query DSL.

    :arg field: Field that the query will target.
    :arg query: Value to find in the provided field.
    :arg options: (Optional) Match additional options as [function named parameters](/reference/query-languages/esql/esql-syntax.md#esql-function-named-params).
    """
    if options is not None:
        return InstrumentedExpression(f"MATCH({field}, {query}, {options})")
    else:
        return InstrumentedExpression(f"MATCH({field}, {query})")


def match_phrase(
    field: ExpressionType, query: ExpressionType, options: ExpressionType = None
) -> InstrumentedExpression:
    """Use `MATCH_PHRASE` to perform a `match_phrase` on the specified field.
    Using `MATCH_PHRASE` is equivalent to using the `match_phrase` query in the
    Elasticsearch Query DSL.

    :arg field: Field that the query will target.
    :arg query: Value to find in the provided field.
    :arg options: (Optional) MatchPhrase additional options as [function named
    parameters](/reference/query-languages/esql/esql-syntax.md#esql-function-named-params).
    See
    [`match_phrase`](/reference/query-languages/query-dsl/query-dsl-match-query-phrase.md)
    for more information.
    """
    if options is not None:
        return InstrumentedExpression(f"MATCH_PHRASE({field}, {query}, {options})")
    else:
        return InstrumentedExpression(f"MATCH_PHRASE({field}, {query})")


def max(field: ExpressionType) -> InstrumentedExpression:
    """The maximum value of a field.

    :arg field:
    """
    return InstrumentedExpression(f"MAX({field})")


def max_over_time(field: ExpressionType) -> InstrumentedExpression:
    """The maximum over time value of a field.

    :arg field:
    """
    return InstrumentedExpression(f"MAX_OVER_TIME({field})")


def md5(input: ExpressionType) -> InstrumentedExpression:
    """Computes the MD5 hash of the input.

    :arg input: Input to hash.
    """
    return InstrumentedExpression(f"MD5({input})")


def median(number: ExpressionType) -> InstrumentedExpression:
    """The value that is greater than half of all values and less than half of
    all values, also known as the 50% `PERCENTILE`.

    :arg number: Expression that outputs values to calculate the median of.
    """
    return InstrumentedExpression(f"MEDIAN({number})")


def median_absolute_deviation(number: ExpressionType) -> InstrumentedExpression:
    """Returns the median absolute deviation, a measure of variability. It is a
    robust statistic, meaning that it is useful for describing data that may
    have outliers, or may not be normally distributed. For such data it can be
    more descriptive than standard deviation.  It is calculated as the median
    of each data point’s deviation from the median of the entire sample. That
    is, for a random variable `X`, the median absolute deviation is
    `median(|median(X) - X|)`.

    :arg number:
    """
    return InstrumentedExpression(f"MEDIAN_ABSOLUTE_DEVIATION({number})")


def min(field: ExpressionType) -> InstrumentedExpression:
    """The minimum value of a field.

    :arg field:
    """
    return InstrumentedExpression(f"MIN({field})")


def min_over_time(field: ExpressionType) -> InstrumentedExpression:
    """The minimum over time value of a field.

    :arg field:
    """
    return InstrumentedExpression(f"MIN_OVER_TIME({field})")


def multi_match(
    query: ExpressionType, fields: ExpressionType, options: ExpressionType = None
) -> InstrumentedExpression:
    """Use `MULTI_MATCH` to perform a multi-match query on the specified field.
    The multi_match query builds on the match query to allow multi-field queries.

    :arg query: Value to find in the provided fields.
    :arg fields: Fields to use for matching
    :arg options: (Optional) Additional options for MultiMatch, passed as
    [function named
    parameters](/reference/query-languages/esql/esql-syntax.md#esql-function-named-params)."
    See [multi-match
    query](/reference/query-languages/query-dsl/query-dsl-match-query.md#query-dsl-multi-match-query)
    for more information.
    """
    if options is not None:
        return InstrumentedExpression(f"MULTI_MATCH({query}, {fields}, {options})")
    else:
        return InstrumentedExpression(f"MULTI_MATCH({query}, {fields})")


def mv_append(field1: ExpressionType, field2: ExpressionType) -> InstrumentedExpression:
    """Concatenates values of two multi-value fields.

    :arg field1:
    :arg field2:
    """
    return InstrumentedExpression(f"MV_APPEND({field1}, {field2})")


def mv_avg(number: ExpressionType) -> InstrumentedExpression:
    """Converts a multivalued field into a single valued field containing the
    average of all of the values.

    :arg number: Multivalue expression.
    """
    return InstrumentedExpression(f"MV_AVG({number})")


def mv_concat(string: ExpressionType, delim: ExpressionType) -> InstrumentedExpression:
    """Converts a multivalued string expression into a single valued column
    containing the concatenation of all values separated by a delimiter.

    :arg string: Multivalue expression.
    :arg delim: Delimiter.
    """
    return InstrumentedExpression(f"MV_CONCAT({string}, {delim})")


def mv_count(field: ExpressionType) -> InstrumentedExpression:
    """Converts a multivalued expression into a single valued column containing
    a count of the number of values.

    :arg field: Multivalue expression.
    """
    return InstrumentedExpression(f"MV_COUNT({field})")


def mv_dedupe(field: ExpressionType) -> InstrumentedExpression:
    """Remove duplicate values from a multivalued field.

    :arg field: Multivalue expression.
    """
    return InstrumentedExpression(f"MV_DEDUPE({field})")


def mv_first(field: ExpressionType) -> InstrumentedExpression:
    """Converts a multivalued expression into a single valued column containing
    the first value. This is most useful when reading from a function that
    emits multivalued columns in a known order like `SPLIT`.

    :arg field: Multivalue expression.
    """
    return InstrumentedExpression(f"MV_FIRST({field})")


def mv_last(field: ExpressionType) -> InstrumentedExpression:
    """Converts a multivalue expression into a single valued column containing
    the last value. This is most useful when reading from a function that emits
    multivalued columns in a known order like `SPLIT`.

    :arg field: Multivalue expression.
    """
    return InstrumentedExpression(f"MV_LAST({field})")


def mv_max(field: ExpressionType) -> InstrumentedExpression:
    """Converts a multivalued expression into a single valued column containing
    the maximum value.

    :arg field: Multivalue expression.
    """
    return InstrumentedExpression(f"MV_MAX({field})")


def mv_median(number: ExpressionType) -> InstrumentedExpression:
    """Converts a multivalued field into a single valued field containing the
    median value.

    :arg number: Multivalue expression.
    """
    return InstrumentedExpression(f"MV_MEDIAN({number})")


def mv_median_absolute_deviation(number: ExpressionType) -> InstrumentedExpression:
    """Converts a multivalued field into a single valued field containing the
    median absolute deviation.  It is calculated as the median of each data
    point’s deviation from the median of the entire sample. That is, for a
    random variable `X`, the median absolute deviation is `median(|median(X) - X|)`.

    :arg number: Multivalue expression.
    """
    return InstrumentedExpression(f"MV_MEDIAN_ABSOLUTE_DEVIATION({number})")


def mv_min(field: ExpressionType) -> InstrumentedExpression:
    """Converts a multivalued expression into a single valued column containing
    the minimum value.

    :arg field: Multivalue expression.
    """
    return InstrumentedExpression(f"MV_MIN({field})")


def mv_percentile(
    number: ExpressionType, percentile: ExpressionType
) -> InstrumentedExpression:
    """Converts a multivalued field into a single valued field containing the
    value at which a certain percentage of observed values occur.

    :arg number: Multivalue expression.
    :arg percentile: The percentile to calculate. Must be a number between 0
    and 100. Numbers out of range will return a null instead.
    """
    return InstrumentedExpression(f"MV_PERCENTILE({number}, {percentile})")


def mv_pseries_weighted_sum(
    number: ExpressionType, p: ExpressionType
) -> InstrumentedExpression:
    """Converts a multivalued expression into a single-valued column by
    multiplying every element on the input list by its corresponding term in
    P-Series and computing the sum.

    :arg number: Multivalue expression.
    :arg p: It is a constant number that represents the *p* parameter in the
    P-Series. It impacts every element’s contribution to the weighted sum.
    """
    return InstrumentedExpression(f"MV_PSERIES_WEIGHTED_SUM({number}, {p})")


def mv_slice(
    field: ExpressionType, start: ExpressionType, end: ExpressionType = None
) -> InstrumentedExpression:
    """Returns a subset of the multivalued field using the start and end index
    values. This is most useful when reading from a function that emits
    multivalued columns in a known order like `SPLIT` or `MV_SORT`.

    :arg field: Multivalue expression. If `null`, the function returns `null`.
    :arg start: Start position. If `null`, the function returns `null`. The
    start argument can be negative. An index of -1 is used to specify the last
    value in the list.
    :arg end: End position(included). Optional; if omitted, the position at
    `start` is returned. The end argument can be negative. An index of -1 is
    used to specify the last value in the list.
    """
    if end is not None:
        return InstrumentedExpression(f"MV_SLICE({field}, {start}, {end})")
    else:
        return InstrumentedExpression(f"MV_SLICE({field}, {start})")


def mv_sort(field: ExpressionType, order: ExpressionType) -> InstrumentedExpression:
    """Sorts a multivalued field in lexicographical order.

    :arg field: Multivalue expression. If `null`, the function returns `null`.
    :arg order: Sort order. The valid options are ASC and DESC, the default is ASC.
    """
    return InstrumentedExpression(f"MV_SORT({field}, {order})")


def mv_sum(number: ExpressionType) -> InstrumentedExpression:
    """Converts a multivalued field into a single valued field containing the
    sum of all of the values.

    :arg number: Multivalue expression.
    """
    return InstrumentedExpression(f"MV_SUM({number})")


def mv_zip(
    string1: ExpressionType, string2: ExpressionType, delim: ExpressionType = None
) -> InstrumentedExpression:
    """Combines the values from two multivalued fields with a delimiter that
    joins them together.

    :arg string1: Multivalue expression.
    :arg string2: Multivalue expression.
    :arg delim: Delimiter. Optional; if omitted, `,` is used as a default delimiter.
    """
    if delim is not None:
        return InstrumentedExpression(f"MV_ZIP({string1}, {string2}, {delim})")
    else:
        return InstrumentedExpression(f"MV_ZIP({string1}, {string2})")


def now() -> InstrumentedExpression:
    """Returns current date and time."""
    return InstrumentedExpression("NOW()")


def percentile(
    number: ExpressionType, percentile: ExpressionType
) -> InstrumentedExpression:
    """Returns the value at which a certain percentage of observed values
    occur. For example, the 95th percentile is the value which is greater than
    95% of the observed values and the 50th percentile is the `MEDIAN`.

    :arg number:
    :arg percentile:
    """
    return InstrumentedExpression(f"PERCENTILE({number}, {percentile})")


def pi() -> InstrumentedExpression:
    """Returns Pi, the ratio of a circle’s circumference to its diameter."""
    return InstrumentedExpression("PI()")


def pow(base: ExpressionType, exponent: ExpressionType) -> InstrumentedExpression:
    """Returns the value of `base` raised to the power of `exponent`.

    :arg base: Numeric expression for the base. If `null`, the function
    returns `null`.
    :arg exponent: Numeric expression for the exponent. If `null`, the function
    returns `null`.
    """
    return InstrumentedExpression(f"POW({base}, {exponent})")


def qstr(
    query: ExpressionType, options: ExpressionType = None
) -> InstrumentedExpression:
    """Performs a query string query. Returns true if the provided query string
    matches the row.

    :arg query: Query string in Lucene query string format.
    :arg options: (Optional) Additional options for Query String as [function
    named
    parameters](/reference/query-languages/esql/esql-syntax.md#esql-function-named-params).
    See [query string
    query](/reference/query-languages/query-dsl/query-dsl-query-string-query.md)
    for more information.
    """
    if options is not None:
        return InstrumentedExpression(f"QSTR({query}, {options})")
    else:
        return InstrumentedExpression(f"QSTR({query})")


def rate(field: ExpressionType) -> InstrumentedExpression:
    """The rate of a counter field.

    :arg field:
    """
    return InstrumentedExpression(f"RATE({field})")


def repeat(string: ExpressionType, number: ExpressionType) -> InstrumentedExpression:
    """Returns a string constructed by concatenating `string` with itself the
    specified `number` of times.

    :arg string: String expression.
    :arg number: Number times to repeat.
    """
    return InstrumentedExpression(f"REPEAT({string}, {number})")


def replace(
    string: ExpressionType, regex: ExpressionType, new_string: ExpressionType
) -> InstrumentedExpression:
    """The function substitutes in the string `str` any match of the regular
    expression `regex` with the replacement string `newStr`.

    :arg string: String expression.
    :arg regex: Regular expression.
    :arg new_string: Replacement string.
    """
    return InstrumentedExpression(f"REPLACE({string}, {regex}, {new_string})")


def reverse(str: ExpressionType) -> InstrumentedExpression:
    """Returns a new string representing the input string in reverse order.

    :arg str: String expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"REVERSE({str})")


def right(string: ExpressionType, length: ExpressionType) -> InstrumentedExpression:
    """Return the substring that extracts *length* chars from *str* starting
    from the right.

    :arg string: The string from which to returns a substring.
    :arg length: The number of characters to return.
    """
    return InstrumentedExpression(f"RIGHT({string}, {length})")


def round(
    number: ExpressionType, decimals: ExpressionType = None
) -> InstrumentedExpression:
    """Rounds a number to the specified number of decimal places. Defaults to
    0, which returns the nearest integer. If the precision is a negative
    number, rounds to the number of digits left of the decimal point.

    :arg number: The numeric value to round. If `null`, the function returns `null`.
    :arg decimals: The number of decimal places to round to. Defaults to 0. If
    `null`, the function returns `null`.
    """
    if decimals is not None:
        return InstrumentedExpression(f"ROUND({number}, {decimals})")
    else:
        return InstrumentedExpression(f"ROUND({number})")


def round_to(field: ExpressionType, points: ExpressionType) -> InstrumentedExpression:
    """Rounds down to one of a list of fixed points.

    :arg field: The numeric value to round. If `null`, the function returns `null`.
    :arg points: Remaining rounding points. Must be constants.
    """
    return InstrumentedExpression(f"ROUND_TO({field}, {points})")


def rtrim(string: ExpressionType) -> InstrumentedExpression:
    """Removes trailing whitespaces from a string.

    :arg string: String expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"RTRIM({string})")


def sample(field: ExpressionType, limit: ExpressionType) -> InstrumentedExpression:
    """Collects sample values for a field.

    :arg field: The field to collect sample values for.
    :arg limit: The maximum number of values to collect.
    """
    return InstrumentedExpression(f"SAMPLE({field}, {limit})")


def scalb(d: ExpressionType, scale_factor: ExpressionType) -> InstrumentedExpression:
    """Returns the result of `d * 2 ^ scaleFactor`, Similar to Java's `scalb`
    function. Result is rounded as if performed by a single correctly rounded
    floating-point multiply to a member of the double value set.

    :arg d: Numeric expression for the multiplier. If `null`, the function
    returns `null`.
    :arg scale_factor: Numeric expression for the scale factor. If `null`, the
    function returns `null`.
    """
    return InstrumentedExpression(f"SCALB({d}, {scale_factor})")


def sha1(input: ExpressionType) -> InstrumentedExpression:
    """Computes the SHA1 hash of the input.

    :arg input: Input to hash.
    """
    return InstrumentedExpression(f"SHA1({input})")


def sha256(input: ExpressionType) -> InstrumentedExpression:
    """Computes the SHA256 hash of the input.

    :arg input: Input to hash.
    """
    return InstrumentedExpression(f"SHA256({input})")


def signum(number: ExpressionType) -> InstrumentedExpression:
    """Returns the sign of the given number. It returns `-1` for negative
    numbers, `0` for `0` and `1` for positive numbers.

    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"SIGNUM({number})")


def sin(angle: ExpressionType) -> InstrumentedExpression:
    """Returns the sine of an angle.

    :arg angle: An angle, in radians. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"SIN({angle})")


def sinh(number: ExpressionType) -> InstrumentedExpression:
    """Returns the hyperbolic sine of a number.

    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"SINH({number})")


def space(number: ExpressionType) -> InstrumentedExpression:
    """Returns a string made of `number` spaces.

    :arg number: Number of spaces in result.
    """
    return InstrumentedExpression(f"SPACE({number})")


def split(string: ExpressionType, delim: ExpressionType) -> InstrumentedExpression:
    """Split a single valued string into multiple strings.

    :arg string: String expression. If `null`, the function returns `null`.
    :arg delim: Delimiter. Only single byte delimiters are currently supported.
    """
    return InstrumentedExpression(f"SPLIT({string}, {delim})")


def sqrt(number: ExpressionType) -> InstrumentedExpression:
    """Returns the square root of a number. The input can be any numeric value,
    the return value is always a double. Square roots of negative numbers and
    infinities are null.

    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"SQRT({number})")


def starts_with(str: ExpressionType, prefix: ExpressionType) -> InstrumentedExpression:
    """Returns a boolean that indicates whether a keyword string starts with
    another string.

    :arg str: String expression. If `null`, the function returns `null`.
    :arg prefix: String expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"STARTS_WITH({str}, {prefix})")


def std_dev(number: ExpressionType) -> InstrumentedExpression:
    """The population standard deviation of a numeric field.

    :arg number:
    """
    return InstrumentedExpression(f"STD_DEV({number})")


def st_centroid_agg(field: ExpressionType) -> InstrumentedExpression:
    """Calculate the spatial centroid over a field with spatial point geometry type.

    :arg field:
    """
    return InstrumentedExpression(f"ST_CENTROID_AGG({field})")


def st_contains(
    geom_a: ExpressionType, geom_b: ExpressionType
) -> InstrumentedExpression:
    """Returns whether the first geometry contains the second geometry. This is
    the inverse of the ST_WITHIN function.

    :arg geom_a: Expression of type `geo_point`, `cartesian_point`,
    `geo_shape` or `cartesian_shape`. If `null`, the function returns `null`.
    :arg geom_b: Expression of type `geo_point`, `cartesian_point`, `geo_shape`
    or `cartesian_shape`. If `null`, the function returns `null`. The second
    parameter must also have the same coordinate system as the first. This
    means it is not possible to combine `geo_*` and `cartesian_*` parameters.
    """
    return InstrumentedExpression(f"ST_CONTAINS({geom_a}, {geom_b})")


def st_disjoint(
    geom_a: ExpressionType, geom_b: ExpressionType
) -> InstrumentedExpression:
    """Returns whether the two geometries or geometry columns are disjoint.
    This is the inverse of the ST_INTERSECTS function. In mathematical terms:
    ST_Disjoint(A, B) ⇔ A ⋂ B = ∅

    :arg geom_a: Expression of type `geo_point`, `cartesian_point`,
    `geo_shape` or `cartesian_shape`. If `null`, the function returns `null`.
    :arg geom_b: Expression of type `geo_point`, `cartesian_point`, `geo_shape`
    or `cartesian_shape`. If `null`, the function returns `null`. The second
    parameter must also have the same coordinate system as the first. This
    means it is not possible to combine `geo_*` and `cartesian_*` parameters.
    """
    return InstrumentedExpression(f"ST_DISJOINT({geom_a}, {geom_b})")


def st_distance(
    geom_a: ExpressionType, geom_b: ExpressionType
) -> InstrumentedExpression:
    """Computes the distance between two points. For cartesian geometries, this
    is the pythagorean distance in the same units as the original coordinates.
    For geographic geometries, this is the circular distance along the great
    circle in meters.

    :arg geom_a: Expression of type `geo_point` or `cartesian_point`. If
    `null`, the function returns `null`.
    :arg geom_b: Expression of type `geo_point` or `cartesian_point`. If
    `null`, the function returns `null`. The second parameter must also have
    the same coordinate system as the first. This means it is not possible to
    combine `geo_point` and `cartesian_point` parameters.
    """
    return InstrumentedExpression(f"ST_DISTANCE({geom_a}, {geom_b})")


def st_envelope(geometry: ExpressionType) -> InstrumentedExpression:
    """Determines the minimum bounding box of the supplied geometry.

    :arg geometry: Expression of type `geo_point`, `geo_shape`,
    `cartesian_point` or `cartesian_shape`. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ST_ENVELOPE({geometry})")


def st_extent_agg(field: ExpressionType) -> InstrumentedExpression:
    """Calculate the spatial extent over a field with geometry type. Returns a
    bounding box for all values of the field.

    :arg field:
    """
    return InstrumentedExpression(f"ST_EXTENT_AGG({field})")


def st_geohash(
    geometry: ExpressionType, precision: ExpressionType, bounds: ExpressionType = None
) -> InstrumentedExpression:
    """Calculates the `geohash` of the supplied geo_point at the specified
    precision. The result is long encoded. Use ST_GEOHASH_TO_STRING to convert
    the result to a string.  These functions are related to the `geo_grid`
    query and the `geohash_grid` aggregation.

    :arg geometry: Expression of type `geo_point`. If `null`, the function
    returns `null`.
    :arg precision: Expression of type `integer`. If `null`, the function
    returns `null`. Valid values are between [1 and 12](https://en.wikipedia.org/wiki/Geohash).
    :arg bounds: Optional bounds to filter the grid tiles, a `geo_shape` of
    type `BBOX`. Use [`ST_ENVELOPE`](#esql-st_envelope) if the `geo_shape` is
    of any other type.
    """
    if bounds is not None:
        return InstrumentedExpression(f"ST_GEOHASH({geometry}, {precision}, {bounds})")
    else:
        return InstrumentedExpression(f"ST_GEOHASH({geometry}, {precision})")


def st_geohash_to_long(grid_id: ExpressionType) -> InstrumentedExpression:
    """Converts an input value representing a geohash grid-ID in string format
    into a long.

    :arg grid_id: Input geohash grid-id. The input can be a single- or
    multi-valued column or an expression.
    """
    return InstrumentedExpression(f"ST_GEOHASH_TO_LONG({grid_id})")


def st_geohash_to_string(grid_id: ExpressionType) -> InstrumentedExpression:
    """Converts an input value representing a geohash grid-ID in long format
    into a string.

    :arg grid_id: Input geohash grid-id. The input can be a single- or
    multi-valued column or an expression.
    """
    return InstrumentedExpression(f"ST_GEOHASH_TO_STRING({grid_id})")


def st_geohex(
    geometry: ExpressionType, precision: ExpressionType, bounds: ExpressionType = None
) -> InstrumentedExpression:
    """Calculates the `geohex`, the H3 cell-id, of the supplied geo_point at
    the specified precision. The result is long encoded. Use
    ST_GEOHEX_TO_STRING to convert the result to a string.  These functions are
    related to the `geo_grid` query and the `geohex_grid` aggregation.

    :arg geometry: Expression of type `geo_point`. If `null`, the function
    returns `null`.
    :arg precision: Expression of type `integer`. If `null`, the function
    returns `null`. Valid values are between [0 and 15](https://h3geo.org/docs/core-library/restable/).
    :arg bounds: Optional bounds to filter the grid tiles, a `geo_shape` of
    type `BBOX`. Use [`ST_ENVELOPE`](#esql-st_envelope) if the `geo_shape` is
    of any other type.
    """
    if bounds is not None:
        return InstrumentedExpression(f"ST_GEOHEX({geometry}, {precision}, {bounds})")
    else:
        return InstrumentedExpression(f"ST_GEOHEX({geometry}, {precision})")


def st_geohex_to_long(grid_id: ExpressionType) -> InstrumentedExpression:
    """Converts an input value representing a geohex grid-ID in string format
    into a long.

    :arg grid_id: Input geohex grid-id. The input can be a single- or
    multi-valued column or an expression.
    """
    return InstrumentedExpression(f"ST_GEOHEX_TO_LONG({grid_id})")


def st_geohex_to_string(grid_id: ExpressionType) -> InstrumentedExpression:
    """Converts an input value representing a Geohex grid-ID in long format
    into a string.

    :arg grid_id: Input Geohex grid-id. The input can be a single- or
    multi-valued column or an expression.
    """
    return InstrumentedExpression(f"ST_GEOHEX_TO_STRING({grid_id})")


def st_geotile(
    geometry: ExpressionType, precision: ExpressionType, bounds: ExpressionType = None
) -> InstrumentedExpression:
    """Calculates the `geotile` of the supplied geo_point at the specified
    precision. The result is long encoded. Use ST_GEOTILE_TO_STRING to convert
    the result to a string.  These functions are related to the `geo_grid`
    query and the `geotile_grid` aggregation.

    :arg geometry: Expression of type `geo_point`. If `null`, the function
    returns `null`.
    :arg precision: Expression of type `integer`. If `null`, the function
    returns `null`. Valid values are between [0 and 29](https://wiki.openstreetmap.org/wiki/Zoom_levels).
    :arg bounds: Optional bounds to filter the grid tiles, a `geo_shape` of
    type `BBOX`. Use [`ST_ENVELOPE`](#esql-st_envelope) if the `geo_shape` is
    of any other type.
    """
    if bounds is not None:
        return InstrumentedExpression(f"ST_GEOTILE({geometry}, {precision}, {bounds})")
    else:
        return InstrumentedExpression(f"ST_GEOTILE({geometry}, {precision})")


def st_geotile_to_long(grid_id: ExpressionType) -> InstrumentedExpression:
    """Converts an input value representing a geotile grid-ID in string format
    into a long.

    :arg grid_id: Input geotile grid-id. The input can be a single- or
    multi-valued column or an expression.
    """
    return InstrumentedExpression(f"ST_GEOTILE_TO_LONG({grid_id})")


def st_geotile_to_string(grid_id: ExpressionType) -> InstrumentedExpression:
    """Converts an input value representing a geotile grid-ID in long format
    into a string.

    :arg grid_id: Input geotile grid-id. The input can be a single- or
    multi-valued column or an expression.
    """
    return InstrumentedExpression(f"ST_GEOTILE_TO_STRING({grid_id})")


def st_intersects(
    geom_a: ExpressionType, geom_b: ExpressionType
) -> InstrumentedExpression:
    """Returns true if two geometries intersect. They intersect if they have
    any point in common, including their interior points (points along lines or
    within polygons). This is the inverse of the ST_DISJOINT function. In
    mathematical terms: ST_Intersects(A, B) ⇔ A ⋂ B ≠ ∅

    :arg geom_a: Expression of type `geo_point`, `cartesian_point`,
    `geo_shape` or `cartesian_shape`. If `null`, the function returns `null`.
    :arg geom_b: Expression of type `geo_point`, `cartesian_point`, `geo_shape`
    or `cartesian_shape`. If `null`, the function returns `null`. The second
    parameter must also have the same coordinate system as the first. This
    means it is not possible to combine `geo_*` and `cartesian_*` parameters.
    """
    return InstrumentedExpression(f"ST_INTERSECTS({geom_a}, {geom_b})")


def st_within(geom_a: ExpressionType, geom_b: ExpressionType) -> InstrumentedExpression:
    """Returns whether the first geometry is within the second geometry. This
    is the inverse of the ST_CONTAINS function.

    :arg geom_a: Expression of type `geo_point`, `cartesian_point`,
    `geo_shape` or `cartesian_shape`. If `null`, the function returns `null`.
    :arg geom_b: Expression of type `geo_point`, `cartesian_point`, `geo_shape`
    or `cartesian_shape`. If `null`, the function returns `null`. The second
    parameter must also have the same coordinate system as the first. This
    means it is not possible to combine `geo_*` and `cartesian_*` parameters.
    """
    return InstrumentedExpression(f"ST_WITHIN({geom_a}, {geom_b})")


def st_x(point: ExpressionType) -> InstrumentedExpression:
    """Extracts the `x` coordinate from the supplied point. If the points is of
    type `geo_point` this is equivalent to extracting the `longitude` value.

    :arg point: Expression of type `geo_point` or `cartesian_point`. If
    `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ST_X({point})")


def st_xmax(point: ExpressionType) -> InstrumentedExpression:
    """Extracts the maximum value of the `x` coordinates from the supplied
    geometry. If the geometry is of type `geo_point` or `geo_shape` this is
    equivalent to extracting the maximum `longitude` value.

    :arg point: Expression of type `geo_point`, `geo_shape`, `cartesian_point`
    or `cartesian_shape`. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ST_XMAX({point})")


def st_xmin(point: ExpressionType) -> InstrumentedExpression:
    """Extracts the minimum value of the `x` coordinates from the supplied
    geometry. If the geometry is of type `geo_point` or `geo_shape` this is
    equivalent to extracting the minimum `longitude` value.

    :arg point: Expression of type `geo_point`, `geo_shape`, `cartesian_point`
    or `cartesian_shape`. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ST_XMIN({point})")


def st_y(point: ExpressionType) -> InstrumentedExpression:
    """Extracts the `y` coordinate from the supplied point. If the points is of
    type `geo_point` this is equivalent to extracting the `latitude` value.

    :arg point: Expression of type `geo_point` or `cartesian_point`. If
    `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ST_Y({point})")


def st_ymax(point: ExpressionType) -> InstrumentedExpression:
    """Extracts the maximum value of the `y` coordinates from the supplied
    geometry. If the geometry is of type `geo_point` or `geo_shape` this is
    equivalent to extracting the maximum `latitude` value.

    :arg point: Expression of type `geo_point`, `geo_shape`, `cartesian_point`
    or `cartesian_shape`. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ST_YMAX({point})")


def st_ymin(point: ExpressionType) -> InstrumentedExpression:
    """Extracts the minimum value of the `y` coordinates from the supplied
    geometry. If the geometry is of type `geo_point` or `geo_shape` this is
    equivalent to extracting the minimum `latitude` value.

    :arg point: Expression of type `geo_point`, `geo_shape`, `cartesian_point`
    or `cartesian_shape`. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"ST_YMIN({point})")


def substring(
    string: ExpressionType, start: ExpressionType, length: ExpressionType = None
) -> InstrumentedExpression:
    """Returns a substring of a string, specified by a start position and an
    optional length.

    :arg string: String expression. If `null`, the function returns `null`.
    :arg start: Start position.
    :arg length: Length of the substring from the start position. Optional; if
    omitted, all positions after `start` are returned.
    """
    if length is not None:
        return InstrumentedExpression(f"SUBSTRING({string}, {start}, {length})")
    else:
        return InstrumentedExpression(f"SUBSTRING({string}, {start})")


def sum(number: ExpressionType) -> InstrumentedExpression:
    """The sum of a numeric expression.

    :arg number:
    """
    return InstrumentedExpression(f"SUM({number})")


def tan(angle: ExpressionType) -> InstrumentedExpression:
    """Returns the tangent of an angle.

    :arg angle: An angle, in radians. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"TAN({angle})")


def tanh(number: ExpressionType) -> InstrumentedExpression:
    """Returns the hyperbolic tangent of a number.

    :arg number: Numeric expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"TANH({number})")


def tau() -> InstrumentedExpression:
    """Returns the ratio of a circle’s circumference to its radius."""
    return InstrumentedExpression("TAU()")


def term(field: ExpressionType, query: ExpressionType) -> InstrumentedExpression:
    """Performs a Term query on the specified field. Returns true if the
    provided term matches the row.

    :arg field: Field that the query will target.
    :arg query: Term you wish to find in the provided field.
    """
    return InstrumentedExpression(f"TERM({field}, {query})")


def top(
    field: ExpressionType, limit: ExpressionType, order: ExpressionType
) -> InstrumentedExpression:
    """Collects the top values for a field. Includes repeated values.

    :arg field: The field to collect the top values for.
    :arg limit: The maximum number of values to collect.
    :arg order: The order to calculate the top values. Either `asc` or `desc`.
    """
    return InstrumentedExpression(f"TOP({field}, {limit}, {order})")


def to_aggregate_metric_double(number: ExpressionType) -> InstrumentedExpression:
    """Encode a numeric to an aggregate_metric_double.

    :arg number: Input value. The input can be a single- or multi-valued
    column or an expression.
    """
    return InstrumentedExpression(f"TO_AGGREGATE_METRIC_DOUBLE({number})")


def to_base64(string: ExpressionType) -> InstrumentedExpression:
    """Encode a string to a base64 string.

    :arg string: A string.
    """
    return InstrumentedExpression(f"TO_BASE64({string})")


def to_boolean(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value to a boolean value. A string value of `true`
    will be case-insensitive converted to the Boolean `true`. For anything
    else, including the empty string, the function will return `false`. The
    numerical value of `0` will be converted to `false`, anything else will be
    converted to `true`.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_BOOLEAN({field})")


def to_cartesianpoint(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value to a `cartesian_point` value. A string will only
    be successfully converted if it respects the WKT Point format.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_CARTESIANPOINT({field})")


def to_cartesianshape(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value to a `cartesian_shape` value. A string will only
    be successfully converted if it respects the WKT format.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_CARTESIANSHAPE({field})")


def to_dateperiod(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value into a `date_period` value.

    :arg field: Input value. The input is a valid constant date period expression.
    """
    return InstrumentedExpression(f"TO_DATEPERIOD({field})")


def to_datetime(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value to a date value. A string will only be
    successfully converted if it’s respecting the format
    `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. To convert dates in other formats, use `DATE_PARSE`.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_DATETIME({field})")


def to_date_nanos(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input to a nanosecond-resolution date value (aka date_nanos).

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_DATE_NANOS({field})")


def to_degrees(number: ExpressionType) -> InstrumentedExpression:
    """Converts a number in radians to degrees).

    :arg number: Input value. The input can be a single- or multi-valued
    column or an expression.
    """
    return InstrumentedExpression(f"TO_DEGREES({number})")


def to_double(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value to a double value. If the input parameter is of
    a date type, its value will be interpreted as milliseconds since the Unix
    epoch, converted to double. Boolean `true` will be converted to double
    `1.0`, `false` to `0.0`.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_DOUBLE({field})")


def to_geopoint(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value to a `geo_point` value. A string will only be
    successfully converted if it respects the WKT Point format.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_GEOPOINT({field})")


def to_geoshape(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value to a `geo_shape` value. A string will only be
    successfully converted if it respects the WKT format.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_GEOSHAPE({field})")


def to_integer(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value to an integer value. If the input parameter is
    of a date type, its value will be interpreted as milliseconds since the
    Unix epoch, converted to integer. Boolean `true` will be converted to
    integer `1`, `false` to `0`.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_INTEGER({field})")


def to_ip(
    field: ExpressionType, options: ExpressionType = None
) -> InstrumentedExpression:
    """Converts an input string to an IP value.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    :arg options: (Optional) Additional options.
    """
    if options is not None:
        return InstrumentedExpression(f"TO_IP({field}, {options})")
    else:
        return InstrumentedExpression(f"TO_IP({field})")


def to_long(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value to a long value. If the input parameter is of a
    date type, its value will be interpreted as milliseconds since the Unix
    epoch, converted to long. Boolean `true` will be converted to long `1`,
    `false` to `0`.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_LONG({field})")


def to_lower(str: ExpressionType) -> InstrumentedExpression:
    """Returns a new string representing the input string converted to lower case.

    :arg str: String expression. If `null`, the function returns `null`. The
    input can be a single-valued column or expression, or a multi-valued column
    or expression {applies_to}`stack: ga 9.1.0`.
    """
    return InstrumentedExpression(f"TO_LOWER({str})")


def to_radians(number: ExpressionType) -> InstrumentedExpression:
    """Converts a number in degrees) to radians.

    :arg number: Input value. The input can be a single- or multi-valued
    column or an expression.
    """
    return InstrumentedExpression(f"TO_RADIANS({number})")


def to_string(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value into a string.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_STRING({field})")


def to_timeduration(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value into a `time_duration` value.

    :arg field: Input value. The input is a valid constant time duration expression.
    """
    return InstrumentedExpression(f"TO_TIMEDURATION({field})")


def to_unsigned_long(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input value to an unsigned long value. If the input
    parameter is of a date type, its value will be interpreted as milliseconds
    since the Unix epoch, converted to unsigned long. Boolean `true` will be
    converted to unsigned long `1`, `false` to `0`.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_UNSIGNED_LONG({field})")


def to_upper(str: ExpressionType) -> InstrumentedExpression:
    """Returns a new string representing the input string converted to upper case.

    :arg str: String expression. If `null`, the function returns `null`. The
    input can be a single-valued column or expression, or a multi-valued column
    or expression {applies_to}`stack: ga 9.1.0`.
    """
    return InstrumentedExpression(f"TO_UPPER({str})")


def to_version(field: ExpressionType) -> InstrumentedExpression:
    """Converts an input string to a version value.

    :arg field: Input value. The input can be a single- or multi-valued column
    or an expression.
    """
    return InstrumentedExpression(f"TO_VERSION({field})")


def trim(string: ExpressionType) -> InstrumentedExpression:
    """Removes leading and trailing whitespaces from a string.

    :arg string: String expression. If `null`, the function returns `null`.
    """
    return InstrumentedExpression(f"TRIM({string})")


def values(field: ExpressionType) -> InstrumentedExpression:
    """Returns unique values as a multivalued field. The order of the returned
    values isn’t guaranteed. If you need the values returned in order use `MV_SORT`.

    :arg field:
    """
    return InstrumentedExpression(f"VALUES({field})")


def weighted_avg(
    number: ExpressionType, weight: ExpressionType
) -> InstrumentedExpression:
    """The weighted average of a numeric expression.

    :arg number: A numeric value.
    :arg weight: A numeric weight.
    """
    return InstrumentedExpression(f"WEIGHTED_AVG({number}, {weight})")
