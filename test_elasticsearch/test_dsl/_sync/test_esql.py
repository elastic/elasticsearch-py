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

from elasticsearch.dsl import Document, M
from elasticsearch.esql import ESQL, functions


class Employee(Document):
    emp_no: M[int]
    first_name: M[str]
    last_name: M[str]
    height: M[float]
    still_hired: M[bool]

    class Index:
        name = "employees"


def load_db():
    data = [
        [10000, "Joseph", "Wall", 2.2, True],
        [10001, "Stephanie", "Ward", 1.749, True],
        [10002, "David", "Keller", 1.872, True],
        [10003, "Roger", "Hinton", 1.694, False],
        [10004, "Joshua", "Garcia", 1.661, False],
        [10005, "Matthew", "Richards", 1.633, False],
        [10006, "Maria", "Luna", 1.893, True],
        [10007, "Angela", "Navarro", 1.604, False],
        [10008, "Maria", "Cannon", 2.079, False],
        [10009, "Joseph", "Sutton", 2.025, True],
    ]
    if Employee._index.exists():
        Employee._index.delete()
    Employee.init()

    for e in data:
        employee = Employee(
            emp_no=e[0], first_name=e[1], last_name=e[2], height=e[3], still_hired=e[4]
        )
        employee.save()
    Employee._index.refresh()


@pytest.mark.sync
def test_esql(client):
    load_db()

    # get the full names of the employees
    query = (
        ESQL.from_(Employee)
        .eval(name=functions.concat(Employee.first_name, " ", Employee.last_name))
        .keep("name")
        .sort("name")
        .limit(10)
    )
    r = client.esql.query(query=str(query))
    assert r.body["values"] == [
        ["Angela Navarro"],
        ["David Keller"],
        ["Joseph Sutton"],
        ["Joseph Wall"],
        ["Joshua Garcia"],
        ["Maria Cannon"],
        ["Maria Luna"],
        ["Matthew Richards"],
        ["Roger Hinton"],
        ["Stephanie Ward"],
    ]

    # get the average height of all hired employees
    query = ESQL.from_(Employee).stats(
        avg_height=functions.round(functions.avg(Employee.height), 2).where(
            Employee.still_hired == True  # noqa: E712
        )
    )
    r = client.esql.query(query=str(query))
    assert r.body["values"] == [[1.95]]
