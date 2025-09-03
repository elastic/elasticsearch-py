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

"""
# ES|QL query builder example

Requirements:

$ pip install elasticsearch faker

To run the example:

$ python esql_employees.py "name to search"

The index will be created automatically with a list of 1000 randomly generated
employees if it does not exist. Add `--recreate-index` or `-r` to the command
to regenerate it.

Examples:

$ python esql_employees "Mark"  # employees named Mark (first or last names)
$ python esql_employees "Sarah" --limit 10  # up to 10 employees named Sarah
$ python esql_employees "Sam" --sort height  # sort results by height
$ python esql_employees "Sam" --sort name  # sort results by last name
"""

import argparse
import os
import random

from faker import Faker

from elasticsearch.dsl import Document, InnerDoc, M, connections
from elasticsearch.esql import ESQLBase
from elasticsearch.esql.functions import concat, multi_match

fake = Faker()


class Address(InnerDoc):
    address: M[str]
    city: M[str]
    zip_code: M[str]


class Employee(Document):
    emp_no: M[int]
    first_name: M[str]
    last_name: M[str]
    height: M[float]
    still_hired: M[bool]
    address: M[Address]

    class Index:
        name = "employees"

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"<Employee[{self.meta.id}]: {self.first_name} {self.last_name}>"


def create(num_employees: int = 1000) -> None:
    print("Creating a new employee index...")
    if Employee._index.exists():
        Employee._index.delete()
    Employee.init()

    for i in range(num_employees):
        address = Address(
            address=fake.address(), city=fake.city(), zip_code=fake.zipcode()
        )
        emp = Employee(
            emp_no=10000 + i,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            height=int((random.random() * 0.8 + 1.5) * 1000) / 1000,
            still_hired=random.random() >= 0.5,
            address=address,
        )
        emp.save()
    Employee._index.refresh()


def search(query: str, limit: int, sort: str) -> None:
    q: ESQLBase = (
        Employee.esql_from()
        .where(multi_match(query, Employee.first_name, Employee.last_name))
        .eval(full_name=concat(Employee.first_name, " ", Employee.last_name))
    )
    if sort == "height":
        q = q.sort(Employee.height.desc())
    elif sort == "name":
        q = q.sort(Employee.last_name.asc())
    q = q.limit(limit)
    for result in Employee.esql_execute(q, return_additional=True):
        assert type(result) == tuple
        employee = result[0]
        full_name = result[1]["full_name"]
        print(
            f"{full_name:<20}",
            f"{'Hired' if employee.still_hired else 'Not hired':<10}",
            f"{employee.height:5.2f}m",
            f"{employee.address.city:<20}",
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Employee ES|QL example")
    parser.add_argument(
        "--recreate-index",
        "-r",
        action="store_true",
        help="Recreate and populate the index",
    )
    parser.add_argument(
        "--limit",
        action="store",
        type=int,
        default=100,
        help="Maximum number or employees to return (default: 100)",
    )
    parser.add_argument(
        "--sort",
        action="store",
        type=str,
        default=None,
        help='Sort by "name" (ascending) or by "height" (descending) (default: no sorting)',
    )
    parser.add_argument(
        "query", action="store", help="The name or partial name to search for"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # initiate the default connection to elasticsearch
    connections.create_connection(hosts=[os.environ["ELASTICSEARCH_URL"]])

    if args.recreate_index or not Employee._index.exists():
        create()
    Employee.init()

    search(args.query, args.limit, args.sort)

    # close the connection
    connections.get_connection().close()


if __name__ == "__main__":
    main()
