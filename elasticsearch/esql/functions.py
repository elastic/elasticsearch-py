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

from elasticsearch.dsl.document_base import InstrumentedExpression


def abs(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the absolutevalue.

    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ABS({number})")


def acos(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the arccosine of `n` as an angle, expressed inradians.

    :arg number: Number between -1 and 1. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ACOS({number})")


def asin(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the arcsine of the input numeric expression as an angle,
    expressed inradians.

    :arg number: Number between -1 and 1. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ASIN({number})")


def atan(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the arctangent of the input numeric expression as an angle,
    expressed inradians.

    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ATAN({number})")


def atan2(
    y_coordinate: InstrumentedExpression, x_coordinate: InstrumentedExpression
) -> InstrumentedExpression:
    """The angle between the positive x-axis and the ray from the origin to the
    point (x , y) in the Cartesian plane, expressed inradians.

    :arg y_coordinate: y coordinate. If `null`, the function returns`null`.
    :arg x_coordinate: x coordinate. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ATAN2({y_coordinate}, {x_coordinate})")


def avg(number: InstrumentedExpression) -> InstrumentedExpression:
    """The average of a numericfield.

    :arg number: Expression that outputs values toaverage.
    """
    return InstrumentedExpression(f"AVG({number})")


def avg_over_time(number: InstrumentedExpression) -> InstrumentedExpression:
    """The average over time of a numericfield.

    :arg number: Expression that outputs values toaverage.
    """
    return InstrumentedExpression(f"AVG_OVER_TIME({number})")


def bit_length(string: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the bit length of astring.

    :arg string: String expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"BIT_LENGTH({string})")


def bucket(
    field: InstrumentedExpression,
    buckets: InstrumentedExpression,
    from_: InstrumentedExpression,
    to: InstrumentedExpression,
) -> InstrumentedExpression:
    """Creates groups of values - buckets - out of a datetime or numeric input.
    The size of the buckets can either be provided directly, or chosen based on
    a recommended count and valuesrange.

    :arg field: Numeric or date expression from which to derivebuckets.
    :arg buckets: Target number of buckets, or desired bucket size if `from`
    and `to` parameters areomitted.
    :arg from_: Start of the range. Can be a number, a date or a date expressed
    as astring.
    :arg to: End of the range. Can be a number, a date or a date expressed as astring.
    """
    return InstrumentedExpression(f"BUCKET({field}, {buckets}, {from_}, {to})")


def byte_length(string: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the byte length of astring.

    :arg string: String expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"BYTE_LENGTH({string})")


def case(
    condition: InstrumentedExpression,
    trueValue: InstrumentedExpression,
    elseValue: InstrumentedExpression,
) -> InstrumentedExpression:
    """Accepts pairs of conditions and values. The function returns the value
    that belongs to the first condition that evaluates to `true`.  If the
    number of arguments is odd, the last argument is the default value which is
    returned when no condition matches. If the number of arguments is even, and
    no condition matches, the function returns`null`.

    :arg condition: Acondition.
    :arg trueValue: The value that’s returned when the corresponding condition
    is the first to evaluate to `true`. The default value is returned when no
    conditionmatches.
    :arg elseValue: The value that’s returned when no condition evaluates to`true`.
    """
    return InstrumentedExpression(f"CASE({condition}, {trueValue}, {elseValue})")


def categorize(field: InstrumentedExpression) -> InstrumentedExpression:
    """Groups text messages into categories of similarly formatted textvalues.

    :arg field: Expression tocategorize
    """
    return InstrumentedExpression(f"CATEGORIZE({field})")


def cbrt(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the cube root of a number. The input can be any numeric value,
    the return value is always a double. Cube roots of infinities arenull.

    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"CBRT({number})")


def ceil(number: InstrumentedExpression) -> InstrumentedExpression:
    """Round a number up to the nearestinteger.

    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"CEIL({number})")


def cidr_match(
    ip: InstrumentedExpression, blockX: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns true if the provided IP is contained in one of the provided CIDRblocks.

    :arg ip: IP address of type `ip` (both IPv4 and IPv6 aresupported).
    :arg blockX: CIDR block to test the IPagainst.
    """
    return InstrumentedExpression(f"CIDR_MATCH({ip}, {blockX})")


def coalesce(
    first: InstrumentedExpression, rest: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns the first of its arguments that is not null. If all arguments
    are null, it returns`null`.

    :arg first: Expression toevaluate.
    :arg rest: Other expression toevaluate.
    """
    return InstrumentedExpression(f"COALESCE({first}, {rest})")


def concat(
    string1: InstrumentedExpression, string2: InstrumentedExpression
) -> InstrumentedExpression:
    """Concatenates two or morestrings.

    :arg string1: Strings toconcatenate.
    :arg string2: Strings toconcatenate.
    """
    return InstrumentedExpression(f"CONCAT({string1}, {string2})")


def cos(angle: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the cosine of anangle.

    :arg angle: An angle, in radians. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"COS({angle})")


def cosh(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the hyperbolic cosine of anumber.

    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"COSH({number})")


def count(field: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the total number (count) of inputvalues.

    :arg field: Expression that outputs values to be counted. If omitted,
    equivalent to `COUNT(*)` (the number ofrows).
    """
    return InstrumentedExpression(f"COUNT({field})")


def count_distinct(
    field: InstrumentedExpression, precision: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns the approximate number of distinctvalues.

    :arg field: Column or literal for which to count the number of distinctvalues.
    :arg precision: Precision threshold. Refer to
    [`AGG-COUNT-DISTINCT-APPROXIMATE`](/reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-agg-count-distinct-approximate).
    The maximum supported value is 40000. Thresholds above this number will
    have the same effect as a threshold of 40000. The default value is3000.
    """
    return InstrumentedExpression(f"COUNT_DISTINCT({field}, {precision})")


def count_distinct_over_time(
    field: InstrumentedExpression, precision: InstrumentedExpression
) -> InstrumentedExpression:
    """The count of distinct values over time for afield.

    :arg field:
    :arg precision: Precision threshold. Refer to
    [`AGG-COUNT-DISTINCT-APPROXIMATE`](/reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-agg-count-distinct-approximate).
    The maximum supported value is 40000. Thresholds above this number will
    have the same effect as a threshold of 40000. The default value is3000.
    """
    return InstrumentedExpression(f"COUNT_DISTINCT_OVER_TIME({field}, {precision})")


def count_over_time(field: InstrumentedExpression) -> InstrumentedExpression:
    """The count over time value of afield.

    :arg field:
    """
    return InstrumentedExpression(f"COUNT_OVER_TIME({field})")


def date_diff(
    unit: InstrumentedExpression,
    startTimestamp: InstrumentedExpression,
    endTimestamp: InstrumentedExpression,
) -> InstrumentedExpression:
    """Subtracts the `startTimestamp` from the `endTimestamp` and returns the
    difference in multiples of `unit`. If `startTimestamp` is later than the
    `endTimestamp`, negative values arereturned.

    :arg unit: Time differenceunit
    :arg startTimestamp: A string representing a starttimestamp
    :arg endTimestamp: A string representing an endtimestamp
    """
    return InstrumentedExpression(
        f"DATE_DIFF({unit}, {startTimestamp}, {endTimestamp})"
    )


def date_extract(
    datePart: InstrumentedExpression, date: InstrumentedExpression
) -> InstrumentedExpression:
    """Extracts parts of a date, like year, month, day,hour.

    :arg datePart: Part of the date to extract.  Can be:
    `aligned_day_of_week_in_month`, `aligned_day_of_week_in_year`,
    `aligned_week_of_month`, `aligned_week_of_year`, `ampm_of_day`,
    `clock_hour_of_ampm`, `clock_hour_of_day`, `day_of_month`, `day_of_week`,
    `day_of_year`, `epoch_day`, `era`, `hour_of_ampm`, `hour_of_day`,
    `instant_seconds`, `micro_of_day`, `micro_of_second`, `milli_of_day`,
    `milli_of_second`, `minute_of_day`, `minute_of_hour`, `month_of_year`,
    `nano_of_day`, `nano_of_second`, `offset_seconds`, `proleptic_month`,
    `second_of_day`, `second_of_minute`, `year`, or `year_of_era`. Refer to
    [java.time.temporal.ChronoField](https://docs.oracle.com/javase/8/docs/api/java/time/temporal/ChronoField.html)
    for a description of these values.  If `null`, the function returns`null`.
    :arg date: Date expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"DATE_EXTRACT({datePart}, {date})")


def date_format(
    dateFormat: InstrumentedExpression, date: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns a string representation of a date, in the providedformat.

    :arg dateFormat: Date format (optional).  If no format is specified, the
    `yyyy-MM-dd'T'HH:mm:ss.SSSZ` format is used. If `null`, the function
    returns`null`.
    :arg date: Date expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"DATE_FORMAT({dateFormat}, {date})")


def date_parse(
    datePattern: InstrumentedExpression, dateString: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns a date by parsing the second argument using the format specified
    in the firstargument.

    :arg datePattern: The date format. Refer to the [`DateTimeFormatter`
    documentation](https://docs.oracle.com/en/java/javase/14/docs/api/java.base/java/time/format/DateTimeFormatter.html)
    for the syntax. If `null`, the function returns`null`.
    :arg dateString: Date expression as a string. If `null` or an empty string,
    the function returns`null`.
    """
    return InstrumentedExpression(f"DATE_PARSE({datePattern}, {dateString})")


def date_trunc(
    interval: InstrumentedExpression, date: InstrumentedExpression
) -> InstrumentedExpression:
    """Rounds down a date to the closest interval since epoch, which starts at`0001-01-01T00:00:00Z`.

    :arg interval: Interval; expressed using the timespan literalsyntax.
    :arg date: Dateexpression
    """
    return InstrumentedExpression(f"DATE_TRUNC({interval}, {date})")


def e() -> InstrumentedExpression:
    """Returns Euler’snumber)."""
    return InstrumentedExpression(f"E()")


def ends_with(
    str: InstrumentedExpression, suffix: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns a boolean that indicates whether a keyword string ends with
    anotherstring.

    :arg str: String expression. If `null`, the function returns`null`.
    :arg suffix: String expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ENDS_WITH({str}, {suffix})")


def exp(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the value of e raised to the power of the givennumber.

    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"EXP({number})")


def first_over_time(field: InstrumentedExpression) -> InstrumentedExpression:
    """The earliest value of a field, where recency determined by the
    `@timestamp`field.

    :arg field:
    """
    return InstrumentedExpression(f"FIRST_OVER_TIME({field})")


def floor(number: InstrumentedExpression) -> InstrumentedExpression:
    """Round a number down to the nearestinteger.

    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"FLOOR({number})")


def from_base64(string: InstrumentedExpression) -> InstrumentedExpression:
    """Decode a base64string.

    :arg string: A base64string.
    """
    return InstrumentedExpression(f"FROM_BASE64({string})")


def greatest(
    first: InstrumentedExpression, rest: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns the maximum value from multiple columns. This is similar to
    `MV_MAX` except it is intended to run on multiple columns atonce.

    :arg first: First of the columns toevaluate.
    :arg rest: The rest of the columns toevaluate.
    """
    return InstrumentedExpression(f"GREATEST({first}, {rest})")


def hash(
    algorithm: InstrumentedExpression, input: InstrumentedExpression
) -> InstrumentedExpression:
    """Computes the hash of the input using various algorithms such as MD5,
    SHA, SHA-224, SHA-256, SHA-384,SHA-512.

    :arg algorithm: Hash algorithm touse.
    :arg input: Input tohash.
    """
    return InstrumentedExpression(f"HASH({algorithm}, {input})")


def hypot(
    number1: InstrumentedExpression, number2: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns the hypotenuse of two numbers. The input can be any numeric
    values, the return value is always a double. Hypotenuses of infinities arenull.

    :arg number1: Numeric expression. If `null`, the function returns`null`.
    :arg number2: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"HYPOT({number1}, {number2})")


def ip_prefix(
    ip: InstrumentedExpression,
    prefixLengthV4: InstrumentedExpression,
    prefixLengthV6: InstrumentedExpression,
) -> InstrumentedExpression:
    """Truncates an IP to a given prefixlength.

    :arg ip: IP address of type `ip` (both IPv4 and IPv6 aresupported).
    :arg prefixLengthV4: Prefix length for IPv4addresses.
    :arg prefixLengthV6: Prefix length for IPv6addresses.
    """
    return InstrumentedExpression(
        f"IP_PREFIX({ip}, {prefixLengthV4}, {prefixLengthV6})"
    )


def knn(
    field: InstrumentedExpression,
    query: InstrumentedExpression,
    options: InstrumentedExpression,
) -> InstrumentedExpression:
    """Finds the k nearest vectors to a query vector, as measured by a
    similarity metric. knn function finds nearest vectors through approximate
    search on indexeddense_vectors.

    :arg field: Field that the query willtarget.
    :arg query: Vector value to find top nearest neighboursfor.
    :arg options: (Optional) kNN additional options as [function named
    parameters](/reference/query-languages/esql/esql-syntax.md#esql-function-named-params).
    See [knn
    query](/reference/query-languages/query-dsl/query-dsl-match-query.md#query-dsl-knn-query)
    for moreinformation.
    """
    return InstrumentedExpression(f"KNN({field}, {query}, {options})")


def kql(query: InstrumentedExpression) -> InstrumentedExpression:
    """Performs a KQL query. Returns true if the provided KQL query string
    matches therow.

    :arg query: Query string in KQL query stringformat.
    """
    return InstrumentedExpression(f"KQL({query})")


def last_over_time(field: InstrumentedExpression) -> InstrumentedExpression:
    """The latest value of a field, where recency determined by the
    `@timestamp`field.

    :arg field:
    """
    return InstrumentedExpression(f"LAST_OVER_TIME({field})")


def least(
    first: InstrumentedExpression, rest: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns the minimum value from multiple columns. This is similar to
    `MV_MIN` except it is intended to run on multiple columns atonce.

    :arg first: First of the columns toevaluate.
    :arg rest: The rest of the columns toevaluate.
    """
    return InstrumentedExpression(f"LEAST({first}, {rest})")


def left(
    string: InstrumentedExpression, length: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns the substring that extracts *length* chars from *string*
    starting from theleft.

    :arg string: The string from which to return asubstring.
    :arg length: The number of characters toreturn.
    """
    return InstrumentedExpression(f"LEFT({string}, {length})")


def length(string: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the character length of astring.

    :arg string: String expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"LENGTH({string})")


def locate(
    string: InstrumentedExpression,
    substring: InstrumentedExpression,
    start: InstrumentedExpression,
) -> InstrumentedExpression:
    """Returns an integer that indicates the position of a keyword substring
    within another string. Returns `0` if the substring cannot be found. Note
    that string positions start from`1`.

    :arg string: An inputstring
    :arg substring: A substring to locate in the inputstring
    :arg start: The startindex
    """
    return InstrumentedExpression(f"LOCATE({string}, {substring}, {start})")


def log(
    base: InstrumentedExpression, number: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns the logarithm of a value to a base. The input can be any numeric
    value, the return value is always a double.  Logs of zero, negative
    numbers, and base of one return `null` as well as awarning.

    :arg base: Base of logarithm. If `null`, the function returns `null`. If
    not provided, this function returns the natural logarithm (base e) of avalue.
    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"LOG({base}, {number})")


def log10(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the logarithm of a value to base 10. The input can be any
    numeric value, the return value is always a double.  Logs of 0 and negative
    numbers return `null` as well as awarning.

    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"LOG10({number})")


def ltrim(string: InstrumentedExpression) -> InstrumentedExpression:
    """Removes leading whitespaces from astring.

    :arg string: String expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"LTRIM({string})")


def match(
    field: InstrumentedExpression,
    query: InstrumentedExpression,
    options: InstrumentedExpression,
) -> InstrumentedExpression:
    """Use `MATCH` to perform a match query on the specified field. Using
    `MATCH` is equivalent to using the `match` query in the Elasticsearch QueryDSL.

    :arg field: Field that the query willtarget.
    :arg query: Value to find in the providedfield.
    :arg options: (Optional) Match additional options as [function namedparameters](/reference/query-languages/esql/esql-syntax.md#esql-function-named-params).
    """
    return InstrumentedExpression(f"MATCH({field}, {query}, {options})")


def match_phrase(
    field: InstrumentedExpression,
    query: InstrumentedExpression,
    options: InstrumentedExpression,
) -> InstrumentedExpression:
    """Use `MATCH_PHRASE` to perform a `match_phrase` on the specified field.
    Using `MATCH_PHRASE` is equivalent to using the `match_phrase` query in the
    Elasticsearch QueryDSL.

    :arg field: Field that the query willtarget.
    :arg query: Value to find in the providedfield.
    :arg options: (Optional) MatchPhrase additional options as [function named
    parameters](/reference/query-languages/esql/esql-syntax.md#esql-function-named-params).
    See
    [`match_phrase`](/reference/query-languages/query-dsl/query-dsl-match-query-phrase.md)
    for moreinformation.
    """
    return InstrumentedExpression(f"MATCH_PHRASE({field}, {query}, {options})")


def max(field: InstrumentedExpression) -> InstrumentedExpression:
    """The maximum value of afield.

    :arg field:
    """
    return InstrumentedExpression(f"MAX({field})")


def max_over_time(field: InstrumentedExpression) -> InstrumentedExpression:
    """The maximum over time value of afield.

    :arg field:
    """
    return InstrumentedExpression(f"MAX_OVER_TIME({field})")


def md5(input: InstrumentedExpression) -> InstrumentedExpression:
    """Computes the MD5 hash of theinput.

    :arg input: Input tohash.
    """
    return InstrumentedExpression(f"MD5({input})")


def median(number: InstrumentedExpression) -> InstrumentedExpression:
    """The value that is greater than half of all values and less than half of
    all values, also known as the 50%`PERCENTILE`.

    :arg number: Expression that outputs values to calculate the medianof.
    """
    return InstrumentedExpression(f"MEDIAN({number})")


def median_absolute_deviation(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the median absolute deviation, a measure of variability. It is a
    robust statistic, meaning that it is useful for describing data that may
    have outliers, or may not be normally distributed. For such data it can be
    more descriptive than standard deviation.  It is calculated as the median
    of each data point’s deviation from the median of the entire sample. That
    is, for a random variable `X`, the median absolute deviation is
    `median(|median(X) -X|)`.

    :arg number:
    """
    return InstrumentedExpression(f"MEDIAN_ABSOLUTE_DEVIATION({number})")


def min(field: InstrumentedExpression) -> InstrumentedExpression:
    """The minimum value of afield.

    :arg field:
    """
    return InstrumentedExpression(f"MIN({field})")


def min_over_time(field: InstrumentedExpression) -> InstrumentedExpression:
    """The minimum over time value of afield.

    :arg field:
    """
    return InstrumentedExpression(f"MIN_OVER_TIME({field})")


def multi_match(
    query: InstrumentedExpression,
    fields: InstrumentedExpression,
    options: InstrumentedExpression,
) -> InstrumentedExpression:
    """Use `MULTI_MATCH` to perform a multi-match query on the specified field.
    The multi_match query builds on the match query to allow multi-fieldqueries.

    :arg query: Value to find in the providedfields.
    :arg fields: Fields to use formatching
    :arg options: (Optional) Additional options for MultiMatch, passed as
    [function named
    parameters](/reference/query-languages/esql/esql-syntax.md#esql-function-named-params)."
    See [multi-match
    query](/reference/query-languages/query-dsl/query-dsl-match-query.md#query-dsl-multi-match-query)
    for moreinformation.
    """
    return InstrumentedExpression(f"MULTI_MATCH({query}, {fields}, {options})")


def mv_append(
    field1: InstrumentedExpression, field2: InstrumentedExpression
) -> InstrumentedExpression:
    """Concatenates values of two multi-valuefields.

    :arg field1:
    :arg field2:
    """
    return InstrumentedExpression(f"MV_APPEND({field1}, {field2})")


def mv_avg(number: InstrumentedExpression) -> InstrumentedExpression:
    """Converts a multivalued field into a single valued field containing the
    average of all of thevalues.

    :arg number: Multivalueexpression.
    """
    return InstrumentedExpression(f"MV_AVG({number})")


def mv_concat(
    string: InstrumentedExpression, delim: InstrumentedExpression
) -> InstrumentedExpression:
    """Converts a multivalued string expression into a single valued column
    containing the concatenation of all values separated by adelimiter.

    :arg string: Multivalueexpression.
    :arg delim:Delimiter.
    """
    return InstrumentedExpression(f"MV_CONCAT({string}, {delim})")


def mv_count(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts a multivalued expression into a single valued column containing
    a count of the number ofvalues.

    :arg field: Multivalueexpression.
    """
    return InstrumentedExpression(f"MV_COUNT({field})")


def mv_dedupe(field: InstrumentedExpression) -> InstrumentedExpression:
    """Remove duplicate values from a multivaluedfield.

    :arg field: Multivalueexpression.
    """
    return InstrumentedExpression(f"MV_DEDUPE({field})")


def mv_first(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts a multivalued expression into a single valued column containing
    the first value. This is most useful when reading from a function that
    emits multivalued columns in a known order like`SPLIT`.

    :arg field: Multivalueexpression.
    """
    return InstrumentedExpression(f"MV_FIRST({field})")


def mv_last(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts a multivalue expression into a single valued column containing
    the last value. This is most useful when reading from a function that emits
    multivalued columns in a known order like`SPLIT`.

    :arg field: Multivalueexpression.
    """
    return InstrumentedExpression(f"MV_LAST({field})")


def mv_max(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts a multivalued expression into a single valued column containing
    the maximumvalue.

    :arg field: Multivalueexpression.
    """
    return InstrumentedExpression(f"MV_MAX({field})")


def mv_median(number: InstrumentedExpression) -> InstrumentedExpression:
    """Converts a multivalued field into a single valued field containing the
    medianvalue.

    :arg number: Multivalueexpression.
    """
    return InstrumentedExpression(f"MV_MEDIAN({number})")


def mv_median_absolute_deviation(
    number: InstrumentedExpression,
) -> InstrumentedExpression:
    """Converts a multivalued field into a single valued field containing the
    median absolute deviation.  It is calculated as the median of each data
    point’s deviation from the median of the entire sample. That is, for a
    random variable `X`, the median absolute deviation is `median(|median(X) -X|)`.

    :arg number: Multivalueexpression.
    """
    return InstrumentedExpression(f"MV_MEDIAN_ABSOLUTE_DEVIATION({number})")


def mv_min(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts a multivalued expression into a single valued column containing
    the minimumvalue.

    :arg field: Multivalueexpression.
    """
    return InstrumentedExpression(f"MV_MIN({field})")


def mv_percentile(
    number: InstrumentedExpression, percentile: InstrumentedExpression
) -> InstrumentedExpression:
    """Converts a multivalued field into a single valued field containing the
    value at which a certain percentage of observed valuesoccur.

    :arg number: Multivalueexpression.
    :arg percentile: The percentile to calculate. Must be a number between 0
    and 100. Numbers out of range will return a nullinstead.
    """
    return InstrumentedExpression(f"MV_PERCENTILE({number}, {percentile})")


def mv_pseries_weighted_sum(
    number: InstrumentedExpression, p: InstrumentedExpression
) -> InstrumentedExpression:
    """Converts a multivalued expression into a single-valued column by
    multiplying every element on the input list by its corresponding term in
    P-Series and computing thesum.

    :arg number: Multivalueexpression.
    :arg p: It is a constant number that represents the *p* parameter in the
    P-Series. It impacts every element’s contribution to the weightedsum.
    """
    return InstrumentedExpression(f"MV_PSERIES_WEIGHTED_SUM({number}, {p})")


def mv_slice(
    field: InstrumentedExpression,
    start: InstrumentedExpression,
    end: InstrumentedExpression,
) -> InstrumentedExpression:
    """Returns a subset of the multivalued field using the start and end index
    values. This is most useful when reading from a function that emits
    multivalued columns in a known order like `SPLIT` or`MV_SORT`.

    :arg field: Multivalue expression. If `null`, the function returns`null`.
    :arg start: Start position. If `null`, the function returns `null`. The
    start argument can be negative. An index of -1 is used to specify the last
    value in thelist.
    :arg end: End position(included). Optional; if omitted, the position at
    `start` is returned. The end argument can be negative. An index of -1 is
    used to specify the last value in thelist.
    """
    return InstrumentedExpression(f"MV_SLICE({field}, {start}, {end})")


def mv_sort(
    field: InstrumentedExpression, order: InstrumentedExpression
) -> InstrumentedExpression:
    """Sorts a multivalued field in lexicographicalorder.

    :arg field: Multivalue expression. If `null`, the function returns`null`.
    :arg order: Sort order. The valid options are ASC and DESC, the default isASC.
    """
    return InstrumentedExpression(f"MV_SORT({field}, {order})")


def mv_sum(number: InstrumentedExpression) -> InstrumentedExpression:
    """Converts a multivalued field into a single valued field containing the
    sum of all of thevalues.

    :arg number: Multivalueexpression.
    """
    return InstrumentedExpression(f"MV_SUM({number})")


def mv_zip(
    string1: InstrumentedExpression,
    string2: InstrumentedExpression,
    delim: InstrumentedExpression,
) -> InstrumentedExpression:
    """Combines the values from two multivalued fields with a delimiter that
    joins themtogether.

    :arg string1: Multivalueexpression.
    :arg string2: Multivalueexpression.
    :arg delim: Delimiter. Optional; if omitted, `,` is used as a defaultdelimiter.
    """
    return InstrumentedExpression(f"MV_ZIP({string1}, {string2}, {delim})")


def now() -> InstrumentedExpression:
    """Returns current date andtime."""
    return InstrumentedExpression(f"NOW()")


def percentile(
    number: InstrumentedExpression, percentile: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns the value at which a certain percentage of observed values
    occur. For example, the 95th percentile is the value which is greater than
    95% of the observed values and the 50th percentile is the`MEDIAN`.

    :arg number:
    :arg percentile:
    """
    return InstrumentedExpression(f"PERCENTILE({number}, {percentile})")


def pi() -> InstrumentedExpression:
    """Returns Pi, the ratio of a circle’s circumference to itsdiameter."""
    return InstrumentedExpression(f"PI()")


def pow(
    base: InstrumentedExpression, exponent: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns the value of `base` raised to the power of`exponent`.

    :arg base: Numeric expression for the base. If `null`, the function
    returns`null`.
    :arg exponent: Numeric expression for the exponent. If `null`, the function
    returns`null`.
    """
    return InstrumentedExpression(f"POW({base}, {exponent})")


def qstr(
    query: InstrumentedExpression, options: InstrumentedExpression
) -> InstrumentedExpression:
    """Performs a query string query. Returns true if the provided query string
    matches therow.

    :arg query: Query string in Lucene query stringformat.
    :arg options: (Optional) Additional options for Query String as [function
    named
    parameters](/reference/query-languages/esql/esql-syntax.md#esql-function-named-params).
    See [query string
    query](/reference/query-languages/query-dsl/query-dsl-query-string-query.md)
    for moreinformation.
    """
    return InstrumentedExpression(f"QSTR({query}, {options})")


def rate(field: InstrumentedExpression) -> InstrumentedExpression:
    """The rate of a counterfield.

    :arg field:
    """
    return InstrumentedExpression(f"RATE({field})")


def repeat(
    string: InstrumentedExpression, number: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns a string constructed by concatenating `string` with itself the
    specified `number` oftimes.

    :arg string: Stringexpression.
    :arg number: Number times torepeat.
    """
    return InstrumentedExpression(f"REPEAT({string}, {number})")


def replace(
    string: InstrumentedExpression,
    regex: InstrumentedExpression,
    newString: InstrumentedExpression,
) -> InstrumentedExpression:
    """The function substitutes in the string `str` any match of the regular
    expression `regex` with the replacement string`newStr`.

    :arg string: Stringexpression.
    :arg regex: Regularexpression.
    :arg newString: Replacementstring.
    """
    return InstrumentedExpression(f"REPLACE({string}, {regex}, {newString})")


def reverse(str: InstrumentedExpression) -> InstrumentedExpression:
    """Returns a new string representing the input string in reverseorder.

    :arg str: String expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"REVERSE({str})")


def right(
    string: InstrumentedExpression, length: InstrumentedExpression
) -> InstrumentedExpression:
    """Return the substring that extracts *length* chars from *str* starting
    from theright.

    :arg string: The string from which to returns asubstring.
    :arg length: The number of characters toreturn.
    """
    return InstrumentedExpression(f"RIGHT({string}, {length})")


def round(
    number: InstrumentedExpression, decimals: InstrumentedExpression
) -> InstrumentedExpression:
    """Rounds a number to the specified number of decimal places. Defaults to
    0, which returns the nearest integer. If the precision is a negative
    number, rounds to the number of digits left of the decimalpoint.

    :arg number: The numeric value to round. If `null`, the function returns`null`.
    :arg decimals: The number of decimal places to round to. Defaults to 0. If
    `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ROUND({number}, {decimals})")


def round_to(
    field: InstrumentedExpression, points: InstrumentedExpression
) -> InstrumentedExpression:
    """Rounds down to one of a list of fixedpoints.

    :arg field: The numeric value to round. If `null`, the function returns`null`.
    :arg points: Remaining rounding points. Must beconstants.
    """
    return InstrumentedExpression(f"ROUND_TO({field}, {points})")


def rtrim(string: InstrumentedExpression) -> InstrumentedExpression:
    """Removes trailing whitespaces from astring.

    :arg string: String expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"RTRIM({string})")


def sample(
    field: InstrumentedExpression, limit: InstrumentedExpression
) -> InstrumentedExpression:
    """Collects sample values for afield.

    :arg field: The field to collect sample valuesfor.
    :arg limit: The maximum number of values tocollect.
    """
    return InstrumentedExpression(f"SAMPLE({field}, {limit})")


def scalb(
    d: InstrumentedExpression, scaleFactor: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns the result of `d * 2 ^ scaleFactor`, Similar to Java's `scalb`
    function. Result is rounded as if performed by a single correctly rounded
    floating-point multiply to a member of the double valueset.

    :arg d: Numeric expression for the multiplier. If `null`, the function
    returns`null`.
    :arg scaleFactor: Numeric expression for the scale factor. If `null`, the
    function returns`null`.
    """
    return InstrumentedExpression(f"SCALB({d}, {scaleFactor})")


def sha1(input: InstrumentedExpression) -> InstrumentedExpression:
    """Computes the SHA1 hash of theinput.

    :arg input: Input tohash.
    """
    return InstrumentedExpression(f"SHA1({input})")


def sha256(input: InstrumentedExpression) -> InstrumentedExpression:
    """Computes the SHA256 hash of theinput.

    :arg input: Input tohash.
    """
    return InstrumentedExpression(f"SHA256({input})")


def signum(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the sign of the given number. It returns `-1` for negative
    numbers, `0` for `0` and `1` for positivenumbers.

    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"SIGNUM({number})")


def sin(angle: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the sine of anangle.

    :arg angle: An angle, in radians. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"SIN({angle})")


def sinh(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the hyperbolic sine of anumber.

    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"SINH({number})")


def space(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns a string made of `number`spaces.

    :arg number: Number of spaces inresult.
    """
    return InstrumentedExpression(f"SPACE({number})")


def split(
    string: InstrumentedExpression, delim: InstrumentedExpression
) -> InstrumentedExpression:
    """Split a single valued string into multiplestrings.

    :arg string: String expression. If `null`, the function returns`null`.
    :arg delim: Delimiter. Only single byte delimiters are currentlysupported.
    """
    return InstrumentedExpression(f"SPLIT({string}, {delim})")


def sqrt(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the square root of a number. The input can be any numeric value,
    the return value is always a double. Square roots of negative numbers and
    infinities arenull.

    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"SQRT({number})")


def starts_with(
    str: InstrumentedExpression, prefix: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns a boolean that indicates whether a keyword string starts with
    anotherstring.

    :arg str: String expression. If `null`, the function returns`null`.
    :arg prefix: String expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"STARTS_WITH({str}, {prefix})")


def std_dev(number: InstrumentedExpression) -> InstrumentedExpression:
    """The population standard deviation of a numericfield.

    :arg number:
    """
    return InstrumentedExpression(f"STD_DEV({number})")


def st_centroid_agg(field: InstrumentedExpression) -> InstrumentedExpression:
    """Calculate the spatial centroid over a field with spatial point geometrytype.

    :arg field:
    """
    return InstrumentedExpression(f"ST_CENTROID_AGG({field})")


def st_contains(
    geomA: InstrumentedExpression, geomB: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns whether the first geometry contains the second geometry. This is
    the inverse of the ST_WITHINfunction.

    :arg geomA: Expression of type `geo_point`, `cartesian_point`, `geo_shape`
    or `cartesian_shape`. If `null`, the function returns`null`.
    :arg geomB: Expression of type `geo_point`, `cartesian_point`, `geo_shape`
    or `cartesian_shape`. If `null`, the function returns `null`. The second
    parameter must also have the same coordinate system as the first. This
    means it is not possible to combine `geo_*` and `cartesian_*`parameters.
    """
    return InstrumentedExpression(f"ST_CONTAINS({geomA}, {geomB})")


def st_disjoint(
    geomA: InstrumentedExpression, geomB: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns whether the two geometries or geometry columns are disjoint.
    This is the inverse of the ST_INTERSECTS function. In mathematical terms:
    ST_Disjoint(A, B) ⇔ A ⋂ B =∅

    :arg geomA: Expression of type `geo_point`, `cartesian_point`, `geo_shape`
    or `cartesian_shape`. If `null`, the function returns`null`.
    :arg geomB: Expression of type `geo_point`, `cartesian_point`, `geo_shape`
    or `cartesian_shape`. If `null`, the function returns `null`. The second
    parameter must also have the same coordinate system as the first. This
    means it is not possible to combine `geo_*` and `cartesian_*`parameters.
    """
    return InstrumentedExpression(f"ST_DISJOINT({geomA}, {geomB})")


def st_distance(
    geomA: InstrumentedExpression, geomB: InstrumentedExpression
) -> InstrumentedExpression:
    """Computes the distance between two points. For cartesian geometries, this
    is the pythagorean distance in the same units as the original coordinates.
    For geographic geometries, this is the circular distance along the great
    circle inmeters.

    :arg geomA: Expression of type `geo_point` or `cartesian_point`. If
    `null`, the function returns`null`.
    :arg geomB: Expression of type `geo_point` or `cartesian_point`. If `null`,
    the function returns `null`. The second parameter must also have the same
    coordinate system as the first. This means it is not possible to combine
    `geo_point` and `cartesian_point`parameters.
    """
    return InstrumentedExpression(f"ST_DISTANCE({geomA}, {geomB})")


def st_envelope(geometry: InstrumentedExpression) -> InstrumentedExpression:
    """Determines the minimum bounding box of the suppliedgeometry.

    :arg geometry: Expression of type `geo_point`, `geo_shape`,
    `cartesian_point` or `cartesian_shape`. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ST_ENVELOPE({geometry})")


def st_extent_agg(field: InstrumentedExpression) -> InstrumentedExpression:
    """Calculate the spatial extent over a field with geometry type. Returns a
    bounding box for all values of thefield.

    :arg field:
    """
    return InstrumentedExpression(f"ST_EXTENT_AGG({field})")


def st_geohash(
    geometry: InstrumentedExpression,
    precision: InstrumentedExpression,
    bounds: InstrumentedExpression,
) -> InstrumentedExpression:
    """Calculates the `geohash` of the supplied geo_point at the specified
    precision. The result is long encoded. Use ST_GEOHASH_TO_STRING to convert
    the result to a string.  These functions are related to the `geo_grid`
    query and the `geohash_grid`aggregation.

    :arg geometry: Expression of type `geo_point`. If `null`, the function
    returns`null`.
    :arg precision: Expression of type `integer`. If `null`, the function
    returns `null`. Valid values are between [1 and12](https://en.wikipedia.org/wiki/Geohash).
    :arg bounds: Optional bounds to filter the grid tiles, a `geo_shape` of
    type `BBOX`. Use [`ST_ENVELOPE`](#esql-st_envelope) if the `geo_shape` is
    of any othertype.
    """
    return InstrumentedExpression(f"ST_GEOHASH({geometry}, {precision}, {bounds})")


def st_geohash_to_long(grid_id: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value representing a geohash grid-ID in string format
    into along.

    :arg grid_id: Input geohash grid-id. The input can be a single- or
    multi-valued column or anexpression.
    """
    return InstrumentedExpression(f"ST_GEOHASH_TO_LONG({grid_id})")


def st_geohash_to_string(grid_id: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value representing a geohash grid-ID in long format
    into astring.

    :arg grid_id: Input geohash grid-id. The input can be a single- or
    multi-valued column or anexpression.
    """
    return InstrumentedExpression(f"ST_GEOHASH_TO_STRING({grid_id})")


def st_geohex(
    geometry: InstrumentedExpression,
    precision: InstrumentedExpression,
    bounds: InstrumentedExpression,
) -> InstrumentedExpression:
    """Calculates the `geohex`, the H3 cell-id, of the supplied geo_point at
    the specified precision. The result is long encoded. Use
    ST_GEOHEX_TO_STRING to convert the result to a string.  These functions are
    related to the `geo_grid` query and the `geohex_grid`aggregation.

    :arg geometry: Expression of type `geo_point`. If `null`, the function
    returns`null`.
    :arg precision: Expression of type `integer`. If `null`, the function
    returns `null`. Valid values are between [0 and15](https://h3geo.org/docs/core-library/restable/).
    :arg bounds: Optional bounds to filter the grid tiles, a `geo_shape` of
    type `BBOX`. Use [`ST_ENVELOPE`](#esql-st_envelope) if the `geo_shape` is
    of any othertype.
    """
    return InstrumentedExpression(f"ST_GEOHEX({geometry}, {precision}, {bounds})")


def st_geohex_to_long(grid_id: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value representing a geohex grid-ID in string format
    into along.

    :arg grid_id: Input geohex grid-id. The input can be a single- or
    multi-valued column or anexpression.
    """
    return InstrumentedExpression(f"ST_GEOHEX_TO_LONG({grid_id})")


def st_geohex_to_string(grid_id: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value representing a Geohex grid-ID in long format
    into astring.

    :arg grid_id: Input Geohex grid-id. The input can be a single- or
    multi-valued column or anexpression.
    """
    return InstrumentedExpression(f"ST_GEOHEX_TO_STRING({grid_id})")


def st_geotile(
    geometry: InstrumentedExpression,
    precision: InstrumentedExpression,
    bounds: InstrumentedExpression,
) -> InstrumentedExpression:
    """Calculates the `geotile` of the supplied geo_point at the specified
    precision. The result is long encoded. Use ST_GEOTILE_TO_STRING to convert
    the result to a string.  These functions are related to the `geo_grid`
    query and the `geotile_grid`aggregation.

    :arg geometry: Expression of type `geo_point`. If `null`, the function
    returns`null`.
    :arg precision: Expression of type `integer`. If `null`, the function
    returns `null`. Valid values are between [0 and29](https://wiki.openstreetmap.org/wiki/Zoom_levels).
    :arg bounds: Optional bounds to filter the grid tiles, a `geo_shape` of
    type `BBOX`. Use [`ST_ENVELOPE`](#esql-st_envelope) if the `geo_shape` is
    of any othertype.
    """
    return InstrumentedExpression(f"ST_GEOTILE({geometry}, {precision}, {bounds})")


def st_geotile_to_long(grid_id: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value representing a geotile grid-ID in string format
    into along.

    :arg grid_id: Input geotile grid-id. The input can be a single- or
    multi-valued column or anexpression.
    """
    return InstrumentedExpression(f"ST_GEOTILE_TO_LONG({grid_id})")


def st_geotile_to_string(grid_id: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value representing a geotile grid-ID in long format
    into astring.

    :arg grid_id: Input geotile grid-id. The input can be a single- or
    multi-valued column or anexpression.
    """
    return InstrumentedExpression(f"ST_GEOTILE_TO_STRING({grid_id})")


def st_intersects(
    geomA: InstrumentedExpression, geomB: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns true if two geometries intersect. They intersect if they have
    any point in common, including their interior points (points along lines or
    within polygons). This is the inverse of the ST_DISJOINT function. In
    mathematical terms: ST_Intersects(A, B) ⇔ A ⋂ B ≠∅

    :arg geomA: Expression of type `geo_point`, `cartesian_point`, `geo_shape`
    or `cartesian_shape`. If `null`, the function returns`null`.
    :arg geomB: Expression of type `geo_point`, `cartesian_point`, `geo_shape`
    or `cartesian_shape`. If `null`, the function returns `null`. The second
    parameter must also have the same coordinate system as the first. This
    means it is not possible to combine `geo_*` and `cartesian_*`parameters.
    """
    return InstrumentedExpression(f"ST_INTERSECTS({geomA}, {geomB})")


def st_within(
    geomA: InstrumentedExpression, geomB: InstrumentedExpression
) -> InstrumentedExpression:
    """Returns whether the first geometry is within the second geometry. This
    is the inverse of the ST_CONTAINSfunction.

    :arg geomA: Expression of type `geo_point`, `cartesian_point`, `geo_shape`
    or `cartesian_shape`. If `null`, the function returns`null`.
    :arg geomB: Expression of type `geo_point`, `cartesian_point`, `geo_shape`
    or `cartesian_shape`. If `null`, the function returns `null`. The second
    parameter must also have the same coordinate system as the first. This
    means it is not possible to combine `geo_*` and `cartesian_*`parameters.
    """
    return InstrumentedExpression(f"ST_WITHIN({geomA}, {geomB})")


def st_x(point: InstrumentedExpression) -> InstrumentedExpression:
    """Extracts the `x` coordinate from the supplied point. If the points is of
    type `geo_point` this is equivalent to extracting the `longitude`value.

    :arg point: Expression of type `geo_point` or `cartesian_point`. If
    `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ST_X({point})")


def st_xmax(point: InstrumentedExpression) -> InstrumentedExpression:
    """Extracts the maximum value of the `x` coordinates from the supplied
    geometry. If the geometry is of type `geo_point` or `geo_shape` this is
    equivalent to extracting the maximum `longitude`value.

    :arg point: Expression of type `geo_point`, `geo_shape`, `cartesian_point`
    or `cartesian_shape`. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ST_XMAX({point})")


def st_xmin(point: InstrumentedExpression) -> InstrumentedExpression:
    """Extracts the minimum value of the `x` coordinates from the supplied
    geometry. If the geometry is of type `geo_point` or `geo_shape` this is
    equivalent to extracting the minimum `longitude`value.

    :arg point: Expression of type `geo_point`, `geo_shape`, `cartesian_point`
    or `cartesian_shape`. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ST_XMIN({point})")


def st_y(point: InstrumentedExpression) -> InstrumentedExpression:
    """Extracts the `y` coordinate from the supplied point. If the points is of
    type `geo_point` this is equivalent to extracting the `latitude`value.

    :arg point: Expression of type `geo_point` or `cartesian_point`. If
    `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ST_Y({point})")


def st_ymax(point: InstrumentedExpression) -> InstrumentedExpression:
    """Extracts the maximum value of the `y` coordinates from the supplied
    geometry. If the geometry is of type `geo_point` or `geo_shape` this is
    equivalent to extracting the maximum `latitude`value.

    :arg point: Expression of type `geo_point`, `geo_shape`, `cartesian_point`
    or `cartesian_shape`. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ST_YMAX({point})")


def st_ymin(point: InstrumentedExpression) -> InstrumentedExpression:
    """Extracts the minimum value of the `y` coordinates from the supplied
    geometry. If the geometry is of type `geo_point` or `geo_shape` this is
    equivalent to extracting the minimum `latitude`value.

    :arg point: Expression of type `geo_point`, `geo_shape`, `cartesian_point`
    or `cartesian_shape`. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"ST_YMIN({point})")


def substring(
    string: InstrumentedExpression,
    start: InstrumentedExpression,
    length: InstrumentedExpression,
) -> InstrumentedExpression:
    """Returns a substring of a string, specified by a start position and an
    optionallength.

    :arg string: String expression. If `null`, the function returns`null`.
    :arg start: Startposition.
    :arg length: Length of the substring from the start position. Optional; if
    omitted, all positions after `start` arereturned.
    """
    return InstrumentedExpression(f"SUBSTRING({string}, {start}, {length})")


def sum(number: InstrumentedExpression) -> InstrumentedExpression:
    """The sum of a numericexpression.

    :arg number:
    """
    return InstrumentedExpression(f"SUM({number})")


def tan(angle: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the tangent of anangle.

    :arg angle: An angle, in radians. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"TAN({angle})")


def tanh(number: InstrumentedExpression) -> InstrumentedExpression:
    """Returns the hyperbolic tangent of anumber.

    :arg number: Numeric expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"TANH({number})")


def tau() -> InstrumentedExpression:
    """Returns the ratio of a circle’s circumference to itsradius."""
    return InstrumentedExpression(f"TAU()")


def term(
    field: InstrumentedExpression, query: InstrumentedExpression
) -> InstrumentedExpression:
    """Performs a Term query on the specified field. Returns true if the
    provided term matches therow.

    :arg field: Field that the query willtarget.
    :arg query: Term you wish to find in the providedfield.
    """
    return InstrumentedExpression(f"TERM({field}, {query})")


def top(
    field: InstrumentedExpression,
    limit: InstrumentedExpression,
    order: InstrumentedExpression,
) -> InstrumentedExpression:
    """Collects the top values for a field. Includes repeatedvalues.

    :arg field: The field to collect the top valuesfor.
    :arg limit: The maximum number of values tocollect.
    :arg order: The order to calculate the top values. Either `asc` or`desc`.
    """
    return InstrumentedExpression(f"TOP({field}, {limit}, {order})")


def to_aggregate_metric_double(
    number: InstrumentedExpression,
) -> InstrumentedExpression:
    """Encode a numeric to anaggregate_metric_double.

    :arg number: Input value. The input can be a single- or multi-valued
    column or anexpression.
    """
    return InstrumentedExpression(f"TO_AGGREGATE_METRIC_DOUBLE({number})")


def to_base64(string: InstrumentedExpression) -> InstrumentedExpression:
    """Encode a string to a base64string.

    :arg string: Astring.
    """
    return InstrumentedExpression(f"TO_BASE64({string})")


def to_boolean(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value to a boolean value. A string value of `true`
    will be case-insensitive converted to the Boolean `true`. For anything
    else, including the empty string, the function will return `false`. The
    numerical value of `0` will be converted to `false`, anything else will be
    converted to`true`.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_BOOLEAN({field})")


def to_cartesianpoint(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value to a `cartesian_point` value. A string will only
    be successfully converted if it respects the WKT Pointformat.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_CARTESIANPOINT({field})")


def to_cartesianshape(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value to a `cartesian_shape` value. A string will only
    be successfully converted if it respects the WKTformat.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_CARTESIANSHAPE({field})")


def to_dateperiod(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value into a `date_period`value.

    :arg field: Input value. The input is a valid constant date periodexpression.
    """
    return InstrumentedExpression(f"TO_DATEPERIOD({field})")


def to_datetime(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value to a date value. A string will only be
    successfully converted if it’s respecting the format
    `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. To convert dates in other formats, use`DATE_PARSE`.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_DATETIME({field})")


def to_date_nanos(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input to a nanosecond-resolution date value (akadate_nanos).

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_DATE_NANOS({field})")


def to_degrees(number: InstrumentedExpression) -> InstrumentedExpression:
    """Converts a number in radians todegrees).

    :arg number: Input value. The input can be a single- or multi-valued
    column or anexpression.
    """
    return InstrumentedExpression(f"TO_DEGREES({number})")


def to_double(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value to a double value. If the input parameter is of
    a date type, its value will be interpreted as milliseconds since the Unix
    epoch, converted to double. Boolean `true` will be converted to double
    `1.0`, `false` to`0.0`.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_DOUBLE({field})")


def to_geopoint(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value to a `geo_point` value. A string will only be
    successfully converted if it respects the WKT Pointformat.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_GEOPOINT({field})")


def to_geoshape(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value to a `geo_shape` value. A string will only be
    successfully converted if it respects the WKTformat.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_GEOSHAPE({field})")


def to_integer(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value to an integer value. If the input parameter is
    of a date type, its value will be interpreted as milliseconds since the
    Unix epoch, converted to integer. Boolean `true` will be converted to
    integer `1`, `false` to`0`.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_INTEGER({field})")


def to_ip(
    field: InstrumentedExpression, options: InstrumentedExpression
) -> InstrumentedExpression:
    """Converts an input string to an IPvalue.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    :arg options: (Optional) Additionaloptions.
    """
    return InstrumentedExpression(f"TO_IP({field}, {options})")


def to_long(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value to a long value. If the input parameter is of a
    date type, its value will be interpreted as milliseconds since the Unix
    epoch, converted to long. Boolean `true` will be converted to long `1`,
    `false` to`0`.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_LONG({field})")


def to_lower(str: InstrumentedExpression) -> InstrumentedExpression:
    """Returns a new string representing the input string converted to lowercase.

    :arg str: String expression. If `null`, the function returns `null`. The
    input can be a single-valued column or expression, or a multi-valued column
    or expression {applies_to}`stack: ga9.1.0`.
    """
    return InstrumentedExpression(f"TO_LOWER({str})")


def to_radians(number: InstrumentedExpression) -> InstrumentedExpression:
    """Converts a number in degrees) toradians.

    :arg number: Input value. The input can be a single- or multi-valued
    column or anexpression.
    """
    return InstrumentedExpression(f"TO_RADIANS({number})")


def to_string(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value into astring.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_STRING({field})")


def to_timeduration(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value into a `time_duration`value.

    :arg field: Input value. The input is a valid constant time durationexpression.
    """
    return InstrumentedExpression(f"TO_TIMEDURATION({field})")


def to_unsigned_long(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input value to an unsigned long value. If the input
    parameter is of a date type, its value will be interpreted as milliseconds
    since the Unix epoch, converted to unsigned long. Boolean `true` will be
    converted to unsigned long `1`, `false` to`0`.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_UNSIGNED_LONG({field})")


def to_upper(str: InstrumentedExpression) -> InstrumentedExpression:
    """Returns a new string representing the input string converted to uppercase.

    :arg str: String expression. If `null`, the function returns `null`. The
    input can be a single-valued column or expression, or a multi-valued column
    or expression {applies_to}`stack: ga9.1.0`.
    """
    return InstrumentedExpression(f"TO_UPPER({str})")


def to_version(field: InstrumentedExpression) -> InstrumentedExpression:
    """Converts an input string to a versionvalue.

    :arg field: Input value. The input can be a single- or multi-valued column
    or anexpression.
    """
    return InstrumentedExpression(f"TO_VERSION({field})")


def trim(string: InstrumentedExpression) -> InstrumentedExpression:
    """Removes leading and trailing whitespaces from astring.

    :arg string: String expression. If `null`, the function returns`null`.
    """
    return InstrumentedExpression(f"TRIM({string})")


def values(field: InstrumentedExpression) -> InstrumentedExpression:
    """Returns unique values as a multivalued field. The order of the returned
    values isn’t guaranteed. If you need the values returned in order use`MV_SORT`.

    :arg field:
    """
    return InstrumentedExpression(f"VALUES({field})")


def weighted_avg(
    number: InstrumentedExpression, weight: InstrumentedExpression
) -> InstrumentedExpression:
    """The weighted average of a numericexpression.

    :arg number: A numericvalue.
    :arg weight: A numericweight.
    """
    return InstrumentedExpression(f"WEIGHTED_AVG({number}, {weight})")
