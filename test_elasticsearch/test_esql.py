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

from elasticsearch.dsl import E
from elasticsearch.esql import ESQL, and_, functions, not_, or_


def test_from():
    query = ESQL.from_("employees")
    assert query.render() == "FROM employees"

    query = ESQL.from_("<logs-{now/d}>")
    assert query.render() == "FROM <logs-{now/d}>"

    query = ESQL.from_("employees-00001", "other-employees-*")
    assert query.render() == "FROM employees-00001, other-employees-*"

    query = ESQL.from_("cluster_one:employees-00001", "cluster_two:other-employees-*")
    assert (
        query.render()
        == "FROM cluster_one:employees-00001, cluster_two:other-employees-*"
    )

    query = ESQL.from_("employees").metadata("_id")
    assert query.render() == "FROM employees METADATA _id"


def test_row():
    query = ESQL.row(a=1, b="two", c=None)
    assert query.render() == 'ROW a = 1, b = "two", c = null'

    query = ESQL.row(a=[2, 1])
    assert query.render() == "ROW a = [2, 1]"

    query = ESQL.row(a=functions.round(1.23, 0))
    assert query.render() == "ROW a = ROUND(1.23, 0)"


def test_show():
    query = ESQL.show("INFO")
    assert query.render() == "SHOW INFO"


def test_change_point():
    query = (
        ESQL.row(key=list(range(1, 26)))
        .mv_expand("key")
        .eval(value=functions.case(E("key") < 13, 0, 42))
        .change_point("value")
        .on("key")
        .where("type IS NOT NULL")
    )
    assert (
        query.render()
        == """ROW key = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
| MV_EXPAND key
| EVAL value = CASE(key < 13, 0, 42)
| CHANGE_POINT value ON key
| WHERE type IS NOT NULL"""
    )


def test_dissect():
    query = (
        ESQL.row(a="2023-01-23T12:15:00.000Z - some text - 127.0.0.1")
        .dissect("a", "%{date} - %{msg} - %{ip}")
        .keep("date", "msg", "ip")
    )
    assert (
        query.render()
        == """ROW a = "2023-01-23T12:15:00.000Z - some text - 127.0.0.1"
| DISSECT a "%{date} - %{msg} - %{ip}"
| KEEP date, msg, ip"""
    )


def test_drop():
    query = ESQL.from_("employees").drop("height")
    assert query.render() == "FROM employees\n| DROP height"
    query = ESQL.from_("employees").drop("height*")
    assert query.render() == "FROM employees\n| DROP height*"


def test_enrich():
    query = ESQL.row(language_code="1").enrich("languages_policy")
    assert (
        query.render()
        == """ROW language_code = "1"
| ENRICH languages_policy"""
    )

    query = ESQL.row(language_code="1").enrich("languages_policy").on("a")
    assert (
        query.render()
        == """ROW language_code = "1"
| ENRICH languages_policy ON a"""
    )

    query = (
        ESQL.row(language_code="1")
        .enrich("languages_policy")
        .on("a")
        .with_(name="language_name")
    )
    assert (
        query.render()
        == """ROW language_code = "1"
| ENRICH languages_policy ON a WITH name = language_name"""
    )


def test_eval():
    query = (
        ESQL.from_("employees")
        .sort("emp_no")
        .keep("first_name", "last_name", "height")
        .eval(height_feet=E("height") * 3.281, height_cm=E("height") * 100)
    )
    assert (
        query.render()
        == """FROM employees
| SORT emp_no
| KEEP first_name, last_name, height
| EVAL height_feet = height * 3.281, height_cm = height * 100"""
    )

    query = (
        ESQL.from_("employees")
        .sort("emp_no")
        .keep("first_name", "last_name", "height")
        .eval(E("height") * 3.281)
    )
    assert (
        query.render()
        == """FROM employees
| SORT emp_no
| KEEP first_name, last_name, height
| EVAL height * 3.281"""
    )

    query = (
        ESQL.from_("employees")
        .eval("height * 3.281")
        .stats(avg_height_feet=functions.avg(E("`height * 3.281`")))
    )
    assert (
        query.render()
        == """FROM employees
| EVAL height * 3.281
| STATS avg_height_feet = AVG(`height * 3.281`)"""
    )


def test_fork():
    query = (
        ESQL.from_("employees")
        .fork(
            ESQL.branch().where(E("emp_no") == 10001),
            ESQL.branch().where("emp_no == 10002"),
        )
        .keep("emp_no", "_fork")
        .sort("emp_no")
    )
    assert (
        query.render()
        == """FROM employees
| FORK ( WHERE emp_no == 10001 )
       ( WHERE emp_no == 10002 )
| KEEP emp_no, _fork
| SORT emp_no"""
    )


def test_grok():
    query = (
        ESQL.row(a="2023-01-23T12:15:00.000Z 127.0.0.1 some.email@foo.com 42")
        .grok(
            "a",
            "%{TIMESTAMP_ISO8601:date} %{IP:ip} %{EMAILADDRESS:email} %{NUMBER:num}",
        )
        .keep("date", "ip", "email", "num")
    )
    assert (
        query.render()
        == """ROW a = "2023-01-23T12:15:00.000Z 127.0.0.1 some.email@foo.com 42"
| GROK a "%{TIMESTAMP_ISO8601:date} %{IP:ip} %{EMAILADDRESS:email} %{NUMBER:num}"
| KEEP date, ip, email, num"""
    )

    query = (
        ESQL.row(a="2023-01-23T12:15:00.000Z 127.0.0.1 some.email@foo.com 42")
        .grok(
            "a",
            "%{TIMESTAMP_ISO8601:date} %{IP:ip} %{EMAILADDRESS:email} %{NUMBER:num:int}",
        )
        .keep("date", "ip", "email", "num")
        .eval(date=functions.to_datetime(E("date")))
    )
    assert (
        query.render()
        == """ROW a = "2023-01-23T12:15:00.000Z 127.0.0.1 some.email@foo.com 42"
| GROK a "%{TIMESTAMP_ISO8601:date} %{IP:ip} %{EMAILADDRESS:email} %{NUMBER:num:int}"
| KEEP date, ip, email, num
| EVAL date = TO_DATETIME(date)"""
    )

    query = (
        ESQL.from_("addresses")
        .keep("city.name", "zip_code")
        .grok("zip_code", "%{WORD:zip_parts} %{WORD:zip_parts}")
    )
    assert (
        query.render()
        == """FROM addresses
| KEEP city.name, zip_code
| GROK zip_code "%{WORD:zip_parts} %{WORD:zip_parts}\""""
    )


def test_keep():
    query = ESQL.from_("employees").keep("emp_no", "first_name", "last_name", "height")
    assert (
        query.render() == "FROM employees\n| KEEP emp_no, first_name, last_name, height"
    )

    query = ESQL.from_("employees").keep("h*")
    assert query.render() == "FROM employees\n| KEEP h*"

    query = ESQL.from_("employees").keep("*", "first_name")
    assert query.render() == "FROM employees\n| KEEP *, first_name"


def test_limit():
    query = ESQL.from_("index").where(E("field") == "value").limit(1000)
    assert query.render() == 'FROM index\n| WHERE field == "value"\n| LIMIT 1000'

    query = (
        ESQL.from_("index").stats(functions.avg(E("field1"))).by("field2").limit(20000)
    )
    assert (
        query.render()
        == "FROM index\n| STATS AVG(field1)\n        BY field2\n| LIMIT 20000"
    )


def test_lookup_join():
    query = (
        ESQL.from_("firewall_logs")
        .lookup_join("threat_list", "source.IP")
        .where("threat_level IS NOT NULL")
    )
    assert (
        query.render()
        == """FROM firewall_logs
| LOOKUP JOIN threat_list ON source.IP
| WHERE threat_level IS NOT NULL"""
    )

    query = (
        ESQL.from_("system_metrics")
        .lookup_join("host_inventory", "host.name")
        .lookup_join("ownerships", "host.name")
    )
    assert (
        query.render()
        == """FROM system_metrics
| LOOKUP JOIN host_inventory ON host.name
| LOOKUP JOIN ownerships ON host.name"""
    )

    query = ESQL.from_("app_logs").lookup_join("service_owners", "service_id")
    assert (
        query.render()
        == """FROM app_logs
| LOOKUP JOIN service_owners ON service_id"""
    )

    query = (
        ESQL.from_("employees")
        .eval(language_code="languages")
        .where(E("emp_no") >= 10091, E("emp_no") < 10094)
        .lookup_join("languages_lookup", "language_code")
    )
    assert (
        query.render()
        == """FROM employees
| EVAL language_code = languages
| WHERE emp_no >= 10091 AND emp_no < 10094
| LOOKUP JOIN languages_lookup ON language_code"""
    )


def test_mv_expand():
    query = ESQL.row(a=[1, 2, 3], b="b", j=["a", "b"]).mv_expand("a")
    assert (
        query.render()
        == """ROW a = [1, 2, 3], b = "b", j = ["a", "b"]
| MV_EXPAND a"""
    )


def test_rename():
    query = (
        ESQL.from_("employees")
        .keep("first_name", "last_name", "still_hired")
        .rename(still_hired="employed")
    )
    assert (
        query.render()
        == """FROM employees
| KEEP first_name, last_name, still_hired
| RENAME still_hired AS employed"""
    )


def test_sample():
    query = ESQL.from_("employees").keep("emp_no").sample(0.05)
    assert (
        query.render()
        == """FROM employees
| KEEP emp_no
| SAMPLE 0.05"""
    )


def test_sort():
    query = (
        ESQL.from_("employees").keep("first_name", "last_name", "height").sort("height")
    )
    assert (
        query.render()
        == """FROM employees
| KEEP first_name, last_name, height
| SORT height"""
    )

    query = (
        ESQL.from_("employees")
        .keep("first_name", "last_name", "height")
        .sort("height DESC")
    )
    assert (
        query.render()
        == """FROM employees
| KEEP first_name, last_name, height
| SORT height DESC"""
    )

    query = (
        ESQL.from_("employees")
        .keep("first_name", "last_name", "height")
        .sort("height DESC", "first_name ASC")
    )
    assert (
        query.render()
        == """FROM employees
| KEEP first_name, last_name, height
| SORT height DESC, first_name ASC"""
    )

    query = (
        ESQL.from_("employees")
        .keep("first_name", "last_name", "height")
        .sort("first_name ASC NULLS FIRST")
    )
    assert (
        query.render()
        == """FROM employees
| KEEP first_name, last_name, height
| SORT first_name ASC NULLS FIRST"""
    )


def test_stats():
    query = (
        ESQL.from_("employees")
        .stats(count=functions.count(E("emp_no")))
        .by("languages")
        .sort("languages")
    )
    assert (
        query.render()
        == """FROM employees
| STATS count = COUNT(emp_no)
        BY languages
| SORT languages"""
    )

    query = ESQL.from_("employees").stats(avg_lang=functions.avg(E("languages")))
    assert (
        query.render()
        == """FROM employees
| STATS avg_lang = AVG(languages)"""
    )

    query = ESQL.from_("employees").stats(
        avg_lang=functions.avg(E("languages")), max_lang=functions.max(E("languages"))
    )
    assert (
        query.render()
        == """FROM employees
| STATS avg_lang = AVG(languages),
        max_lang = MAX(languages)"""
    )

    query = (
        ESQL.from_("employees")
        .stats(
            avg50s=functions.avg(E("salary")).where('birth_date < "1960-01-01"'),
            avg60s=functions.avg(E("salary")).where('birth_date >= "1960-01-01"'),
        )
        .by("gender")
        .sort("gender")
    )
    assert (
        query.render()
        == """FROM employees
| STATS avg50s = AVG(salary) WHERE birth_date < "1960-01-01",
        avg60s = AVG(salary) WHERE birth_date >= "1960-01-01"
        BY gender
| SORT gender"""
    )

    query = (
        ESQL.from_("employees")
        .eval(Ks="salary / 1000")
        .stats(
            under_40K=functions.count(E("*")).where("Ks < 40"),
            inbetween=functions.count(E("*")).where("40 <= Ks", "Ks < 60"),
            over_60K=functions.count(E("*")).where("60 <= Ks"),
            total=functions.count(E("*")),
        )
    )
    assert (
        query.render()
        == """FROM employees
| EVAL Ks = salary / 1000
| STATS under_40K = COUNT(*) WHERE Ks < 40,
        inbetween = COUNT(*) WHERE (40 <= Ks) AND (Ks < 60),
        over_60K = COUNT(*) WHERE 60 <= Ks,
        total = COUNT(*)"""
    )

    query = (
        ESQL.row(i=1, a=["a", "b"]).stats(functions.min(E("i"))).by("a").sort("a ASC")
    )
    assert (
        query.render()
        == 'ROW i = 1, a = ["a", "b"]\n| STATS MIN(i)\n        BY a\n| SORT a ASC'
    )

    query = (
        ESQL.from_("employees")
        .eval(hired=functions.date_format(E("hire_date"), "yyyy"))
        .stats(avg_salary=functions.avg(E("salary")))
        .by("hired", "languages.long")
        .eval(avg_salary=functions.round(E("avg_salary")))
        .sort("hired", "languages.long")
    )
    assert (
        query.render()
        == """FROM employees
| EVAL hired = DATE_FORMAT("yyyy", hire_date)
| STATS avg_salary = AVG(salary)
        BY hired, languages.long
| EVAL avg_salary = ROUND(avg_salary)
| SORT hired, languages.long"""
    )


def test_where():
    query = (
        ESQL.from_("employees")
        .keep("first_name", "last_name", "still_hired")
        .where("still_hired == true")
    )
    assert (
        query.render()
        == """FROM employees
| KEEP first_name, last_name, still_hired
| WHERE still_hired == true"""
    )

    query = ESQL.from_("sample_data").where("@timestamp > NOW() - 1 hour")
    assert (
        query.render()
        == """FROM sample_data
| WHERE @timestamp > NOW() - 1 hour"""
    )

    query = (
        ESQL.from_("employees")
        .keep("first_name", "last_name", "height")
        .where("LENGTH(first_name) < 4")
    )
    assert (
        query.render()
        == """FROM employees
| KEEP first_name, last_name, height
| WHERE LENGTH(first_name) < 4"""
    )


def test_and_operator():
    query = ESQL.from_("index").where(
        and_(E("age") > 30, E("age") < 40, E("name").is_not_null())
    )
    assert (
        query.render()
        == """FROM index
| WHERE (age > 30) AND (age < 40) AND (name IS NOT NULL)"""
    )


def test_or_operator():
    query = ESQL.from_("index").where(
        or_(E("age") < 30, E("age") > 40, E("name").is_null())
    )
    assert (
        query.render()
        == """FROM index
| WHERE (age < 30) OR (age > 40) OR (name IS NULL)"""
    )


def test_not_operator():
    query = ESQL.from_("index").where(not_(E("age") > 40))
    assert (
        query.render()
        == """FROM index
| WHERE NOT (age > 40)"""
    )


def test_in_operator():
    query = ESQL.row(a=1, b=4, c=3).where((E("c") - E("a")).in_(3, E("b") / 2, "a"))
    assert (
        query.render()
        == """ROW a = 1, b = 4, c = 3
| WHERE c - a IN (3, b / 2, a)"""
    )


def test_like_operator():
    query = (
        ESQL.from_("employees")
        .where(E("first_name").like("?b*"))
        .keep("first_name", "last_name")
    )
    assert (
        query.render()
        == """FROM employees
| WHERE first_name LIKE "?b*"
| KEEP first_name, last_name"""
    )

    query = ESQL.row(message="foo * bar").where(E("message").like("foo \\* bar"))
    assert (
        query.render()
        == """ROW message = "foo * bar"
| WHERE message LIKE "foo \\\\* bar\""""
    )

    query = ESQL.row(message="foobar").where(E("message").like("foo*", "bar?"))
    assert (
        query.render()
        == """ROW message = "foobar"
| WHERE message LIKE ("foo*", "bar?")"""
    )


def test_rlike_operator():
    query = (
        ESQL.from_("employees")
        .where(E("first_name").rlike(".leja*"))
        .keep("first_name", "last_name")
    )
    assert (
        query.render()
        == """FROM employees
| WHERE first_name RLIKE ".leja*"
| KEEP first_name, last_name"""
    )

    query = ESQL.row(message="foo ( bar").where(E("message").rlike("foo \\( bar"))
    assert (
        query.render()
        == """ROW message = "foo ( bar"
| WHERE message RLIKE "foo \\\\( bar\""""
    )

    query = ESQL.row(message="foobar").where(E("message").rlike("foo.*", "bar."))
    assert (
        query.render()
        == """ROW message = "foobar"
| WHERE message RLIKE ("foo.*", "bar.")"""
    )


def test_match_operator():
    query = ESQL.from_("books").where(E("author").match("Faulkner"))
    assert (
        query.render()
        == """FROM books
| WHERE author:"Faulkner\""""
    )
