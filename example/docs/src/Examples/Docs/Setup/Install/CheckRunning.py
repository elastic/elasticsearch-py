#!/usr/bin/env python

'''
Licensed to Elasticsearch B.V under one or more agreements.
Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
See the LICENSE file in the project root for more information
'''

from elasticsearch import Elasticsearch

es = Elasticsearch()

print("3d1ff6097e2359f927c88c2ccdb36252 - L:7")
# tag::3d1ff6097e2359f927c88c2ccdb36252[]
response = es.info()
# end::3d1ff6097e2359f927c88c2ccdb36252[]
print("---------------------------------------")
print(response)
print("---------------------------------------")
