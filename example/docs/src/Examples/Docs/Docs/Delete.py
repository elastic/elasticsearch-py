#!/usr/bin/env python

'''
Licensed to Elasticsearch B.V under one or more agreements.
Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
See the LICENSE file in the project root for more information
'''

from elasticsearch import Elasticsearch

es = Elasticsearch()

print("c5e5873783246c7b1c01d8464fed72c4 - L:9")
# tag::c5e5873783246c7b1c01d8464fed72c4[]
response = es.delete(
    index='twitter',
    id=1,
)
# end::c5e5873783246c7b1c01d8464fed72c4[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("47b5ff897f26e9c943cee5c06034181d - L:84")
# tag::47b5ff897f26e9c943cee5c06034181d[]
response = es.delete(
    index='twitter',
    id=1,
    routing='kimchy',
)
# end::47b5ff897f26e9c943cee5c06034181d[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("d90a84a24a407731dfc1929ac8327746 - L:147")
# tag::d90a84a24a407731dfc1929ac8327746[]
response = es.delete(
    index='twitter',
    id=1,
    timeout='5m',
)
# end::d90a84a24a407731dfc1929ac8327746[]
print("---------------------------------------")
print(response)
print("---------------------------------------")
