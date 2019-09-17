#!/usr/bin/env python

'''
Licensed to Elasticsearch B.V under one or more agreements.
Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
See the LICENSE file in the project root for more information
'''

from elasticsearch import Elasticsearch

es = Elasticsearch()

print("fbcf5078a6a9e09790553804054c36b3 - L:9")
# tag::fbcf5078a6a9e09790553804054c36b3[]
response = es.get(
    index='twitter',
    id=0,
)
# end::fbcf5078a6a9e09790553804054c36b3[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("98234499cfec70487cec5d013e976a84 - L:46")
# tag::98234499cfec70487cec5d013e976a84[]
response = es.exists(
    index='twitter',
    id=0,
)
# end::98234499cfec70487cec5d013e976a84[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("138ccd89f72aa7502dd9578403dcc589 - L:72")
# tag::138ccd89f72aa7502dd9578403dcc589[]
response = es.get(
    index='twitter',
    id=0,
    _source=False,
)
# end::138ccd89f72aa7502dd9578403dcc589[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("8fdf2344c4fb3de6902ad7c5735270df - L:84")
# tag::8fdf2344c4fb3de6902ad7c5735270df[]
response = es.get(
    index='twitter',
    id=0,
    _source_includes='*.id',
    _source_excludes='entities',
)
# end::8fdf2344c4fb3de6902ad7c5735270df[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("745f9b8cdb8e91073f6e520e1d9f8c05 - L:93")
# tag::745f9b8cdb8e91073f6e520e1d9f8c05[]
response = es.get(
    index='twitter',
    id=0,
    _source='*.id,retweeted',
)
# end::745f9b8cdb8e91073f6e520e1d9f8c05[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("913770050ebbf3b9b549a899bc11060a - L:109")
print("TODO")

print("5eabcdbf61bfcb484dc694f25c2bba36 - L:131")
# tag::5eabcdbf61bfcb484dc694f25c2bba36[]
response = es.index(
    index='twitter',
    id=1,
    body={
        'counter': 1,
        'tags': ['red'],
    },
)
# end::5eabcdbf61bfcb484dc694f25c2bba36[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("710c7871f20f176d51209b1574b0d61b - L:144")
# tag::710c7871f20f176d51209b1574b0d61b[]
response = es.get(
    index='twitter',
    id=1,
    stored_fields='tags,counter',
)
# end::710c7871f20f176d51209b1574b0d61b[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("0ba0b2db24852abccb7c0fc1098d566e - L:178")
# tag::0ba0b2db24852abccb7c0fc1098d566e[]
response = es.index(
    index='twitter',
    id=1,
    body={
        'counter': 1,
        'tags': ['white'],
    },
    routing='user1',
)
# end::0ba0b2db24852abccb7c0fc1098d566e[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("69a7be47f85138b10437113ab2f0d72d - L:189")
# tag::69a7be47f85138b10437113ab2f0d72d[]
response = es.get(
    index='twitter',
    id=2,
    routing='user1',
    stored_fields='tags,counter',
)
# end::69a7be47f85138b10437113ab2f0d72d[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("89a8ac1509936acc272fc2d72907bc45 - L:229")
# tag::89a8ac1509936acc272fc2d72907bc45[]
response = es.get_source(
    index='twitter',
    id=1,
)
# end::89a8ac1509936acc272fc2d72907bc45[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("d222c6a6ec7a3beca6c97011b0874512 - L:238")
# tag::d222c6a6ec7a3beca6c97011b0874512[]
response = es.get_source(
    index='twitter',
    id=1,
    _source_includes='*.id',
    _source_excludes='entities',
)
# end::d222c6a6ec7a3beca6c97011b0874512[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("2468ab381257d759d8a88af1141f6f9c - L:248")
print("TODO")

print("1d65cb6d055c46a1bde809687d835b71 - L:262")
# tag::1d65cb6d055c46a1bde809687d835b71[]
response = es.get(
    index='twitter',
    id=1,
    routing='user1',
)
# end::1d65cb6d055c46a1bde809687d835b71[]
print("---------------------------------------")
print(response)
print("---------------------------------------")
