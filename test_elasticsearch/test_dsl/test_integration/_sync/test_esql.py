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

from elasticsearch.dsl import Document, InnerDoc, M
from elasticsearch.esql import ESQL, E, functions


class Address(InnerDoc):
    address: M[str]
    city: M[str]


class Employee(Document):
    emp_no: M[int]
    first_name: M[str]
    last_name: M[str]
    height: M[float]
    still_hired: M[bool]
    address: M[Address]

    class Index:
        name = "employees"


def load_db():
    data = [
        [
            10000,
            "Joseph",
            "Wall",
            2.2,
            True,
            Address(address="8875 Long Shoals Suite 441", city="Marcville, TX"),
        ],
        [
            10001,
            "Stephanie",
            "Ward",
            1.749,
            True,
            Address(address="90162 Carter Harbor Suite 099", city="Davisborough, DE"),
        ],
        [
            10002,
            "David",
            "Keller",
            1.872,
            True,
            Address(address="6697 Patrick Union Suite 797", city="Fuentesmouth, SD"),
        ],
        [
            10003,
            "Roger",
            "Hinton",
            1.694,
            False,
            Address(address="809 Kelly Mountains", city="South Megan, DE"),
        ],
        [
            10004,
            "Joshua",
            "Garcia",
            1.661,
            False,
            Address(address="718 Angela Forks", city="Port Erinland, MA"),
        ],
        [
            10005,
            "Matthew",
            "Richards",
            1.633,
            False,
            Address(address="2869 Brown Mountains", city="New Debra, NH"),
        ],
        [
            10006,
            "Maria",
            "Luna",
            1.893,
            True,
            Address(address="5861 Morgan Springs", city="Lake Daniel, WI"),
        ],
        [
            10007,
            "Angela",
            "Navarro",
            1.604,
            False,
            Address(address="2848 Allen Station", city="Saint Joseph, OR"),
        ],
        [
            10008,
            "Maria",
            "Cannon",
            2.079,
            False,
            Address(address="322 NW Johnston", city="Bakerburgh, MP"),
        ],
        [
            10009,
            "Joseph",
            "Sutton",
            2.025,
            True,
            Address(address="77 Cardinal E", city="Lakestown, IL"),
        ],
    ]
    if Employee._index.exists():
        Employee._index.delete()
    Employee.init()

    for e in data:
        employee = Employee(
            emp_no=e[0],
            first_name=e[1],
            last_name=e[2],
            height=e[3],
            still_hired=e[4],
            address=e[5],
        )
        employee.save()
    Employee._index.refresh()


@pytest.mark.sync
def test_esql(client):
    load_db()

    # get the full names of the employees
    query = (
        ESQL.from_(Employee)
        .eval(full_name=functions.concat(Employee.first_name, " ", Employee.last_name))
        .keep("full_name")
        .sort("full_name")
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

    # find employees by name using a parameter
    query = (
        ESQL.from_(Employee)
        .where(Employee.first_name == E("?"))
        .keep(Employee.last_name)
        .sort(Employee.last_name.desc())
    )
    r = client.esql.query(query=str(query), params=["Maria"])
    assert r.body["values"] == [["Luna"], ["Cannon"]]


@pytest.mark.sync
def test_esql_dsl(client):
    load_db()

    # get employees with first name "Maria"
    query = (
        Employee.esql_from()
        .where(Employee.first_name == "Maria")
        .sort("last_name")
        .limit(10)
    )
    marias = []
    for emp in Employee.esql_execute(query):
        marias.append(emp)
    assert len(marias) == 2
    assert marias[0].last_name == "Cannon"
    assert marias[0].address.address == "322 NW Johnston"
    assert marias[0].address.city == "Bakerburgh, MP"
    assert marias[1].last_name == "Luna"
    assert marias[1].address.address == "5861 Morgan Springs"
    assert marias[1].address.city == "Lake Daniel, WI"

    # run a query with a missing field
    query = (
        Employee.esql_from()
        .where(Employee.first_name == "Maria")
        .drop(Employee.address.city)
        .sort("last_name")
        .limit(10)
    )
    with pytest.raises(ValueError):
        Employee.esql_execute(query).__next__()
    marias = []
    for emp in Employee.esql_execute(query, ignore_missing_fields=True):
        marias.append(emp)
    assert marias[0].last_name == "Cannon"
    assert marias[0].address.address == "322 NW Johnston"
    assert marias[0].address.city is None
    assert marias[1].last_name == "Luna"
    assert marias[1].address.address == "5861 Morgan Springs"
    assert marias[1].address.city is None

    # run a query with additional calculated fields
    query = (
        Employee.esql_from()
        .where(Employee.first_name == "Maria")
        .eval(
            full_name=functions.concat(Employee.first_name, " ", Employee.last_name),
            height_cm=functions.to_integer(Employee.height * 100),
        )
        .sort("last_name")
        .limit(10)
    )
    assert isinstance(Employee.esql_execute(query).__next__(), Employee)
    assert isinstance(
        Employee.esql_execute(query, return_additional=True).__next__(), tuple
    )
    marias = []
    for emp, extra in Employee.esql_execute(query, return_additional=True):
        marias.append([emp, extra])
    assert marias[0][0].last_name == "Cannon"
    assert marias[0][0].address.address == "322 NW Johnston"
    assert marias[0][0].address.city == "Bakerburgh, MP"
    assert marias[0][1] == {"full_name": "Maria Cannon", "height_cm": 208}
    assert marias[1][0].last_name == "Luna"
    assert marias[1][0].address.address == "5861 Morgan Springs"
    assert marias[1][0].address.city == "Lake Daniel, WI"
    assert marias[1][1] == {"full_name": "Maria Luna", "height_cm": 189}
