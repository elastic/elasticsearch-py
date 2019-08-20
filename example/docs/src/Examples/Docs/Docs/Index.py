#!/usr/bin/env python

'''
Licensed to Elasticsearch B.V under one or more agreements.
Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
See the LICENSE file in the project root for more information
'''

from elasticsearch import Elasticsearch

es = Elasticsearch()

print("bb143628fd04070683eeeadc9406d9cc - L:11")
# tag::bb143628fd04070683eeeadc9406d9cc[]
response = es.index(
    index='twitter',
    id=1,
    body={
        'user': 'kimchy',
        'post_date': '2009-11-15T14:12:12',
        'message': 'trying out Elasticsearch',
    }
)
# end::bb143628fd04070683eeeadc9406d9cc[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("804a97ff4d0613e6568e4efb19c52021 - L:77")
print("TODO")

print("d718b63cf1b6591a1d59a0cf4fd995eb - L:121")
# tag::d718b63cf1b6591a1d59a0cf4fd995eb[]
response = es.index(
    index='twitter',
    id=1,
    body={
        'user': 'kimchy',
        'post_date': '2009-11-15T14:12:12',
        'message': 'trying out Elasticsearch',
    },
    op_type='create',
)
# end::d718b63cf1b6591a1d59a0cf4fd995eb[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("048d8abd42d094bbdcf4452a58ccb35b - L.:134")
# tag::048d8abd42d094bbdcf4452a58ccb35b[]
response = es.create(
    index='twitter',
    id=1,
    body={
        'user': 'kimchy',
        'post_date': '2009-11-15T14:12:12',
        'message': 'trying out Elasticsearch',
    }
)
# end::048d8abd42d094bbdcf4452a58ccb35b[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("36818c6d9f434d387819c30bd9addb14 - L:153")
# tag::36818c6d9f434d387819c30bd9addb14[]
response = es.index(
    index='twitter',
    body={
        'user': 'kimchy',
        'post_date': '2009-11-15T14:12:12',
        'message': 'trying out Elasticsearch',
    }
)
# end::36818c6d9f434d387819c30bd9addb14[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("625dc94df1f9affb49a082fd99d41620 - L:204")
# tag::625dc94df1f9affb49a082fd99d41620[]
response = es.index(
    index='twitter',
    id=1,
    body={
        'user': 'kimchy',
        'post_date': '2009-11-15T14:12:12',
        'message': 'trying out Elasticsearch',
    },
    routing='kimchy',
)
# end::625dc94df1f9affb49a082fd99d41620[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("b918d6b798da673a33e49b94f61dcdc0 - L:327")
# tag::b918d6b798da673a33e49b94f61dcdc0[]
response = es.index(
    index='twitter',
    id=1,
    body={
        'user': 'kimchy',
        'post_date': '2009-11-15T14:12:12',
        'message': 'trying out Elasticsearch',
    },
    timeout='5m',
)
# end::b918d6b798da673a33e49b94f61dcdc0[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("1f336ecc62480c1d56351cc2f82d0d08 - L:357")
# tag::1f336ecc62480c1d56351cc2f82d0d08[]
response = es.index(
    index='twitter',
    id=1,
    body={
        'user': 'kimchy',
        'post_date': '2009-11-15T14:12:12',
        'message': 'trying out Elasticsearch',
    },
    version=2,
    version_type='external',
)
# end::1f336ecc62480c1d56351cc2f82d0d08[]
print("---------------------------------------")
print(response)
print("---------------------------------------")
