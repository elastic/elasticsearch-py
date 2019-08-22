#!/usr/bin/env python

'''
Licensed to Elasticsearch B.V under one or more agreements.
Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
See the LICENSE file in the project root for more information
'''

from elasticsearch import Elasticsearch

es = Elasticsearch()

print("f8cc4b331a19ff4df8e4a490f906ee69 - L: 209")
# tag::f8cc4b331a19ff4df8e4a490f906ee69[]
response = es.cat.health(v=True)
# end::f8cc4b331a19ff4df8e4a490f906ee69[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("db20adb70a8e8d0709d15ba0daf18d23 - L:240")
# tag::db20adb70a8e8d0709d15ba0daf18d23[]
response = es.cat.nodes(v=True)
# end::db20adb70a8e8d0709d15ba0daf18d23[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("c3fa04519df668d6c27727a12ab09648 - L:263")
# tag::c3fa04519df668d6c27727a12ab09648[]
response = es.cat.indices(v=True)
# end::c3fa04519df668d6c27727a12ab09648[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("0caf6b6b092ecbcf6f996053678a2384 - L:284")
# tag::0caf6b6b092ecbcf6f996053678a2384[]
#        // PUT /customer?pretty
response = es.cat.indices(v=True)
# end::0caf6b6b092ecbcf6f996053678a2384[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("21fe98843fe0b5473f515d21803db409 - L:311")
# tag::21fe98843fe0b5473f515d21803db409[]
response = es.index(
    index='customer',
    id=1,
    body={
        'name': 'John Doe',
    }
)
# end::21fe98843fe0b5473f515d21803db409[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("37a3b66b555aed55618254f50d572cd6 - L:347")
# tag::37a3b66b555aed55618254f50d572cd6[]
response = es.get(
    index='customer',
    id=1,
)
# end::37a3b66b555aed55618254f50d572cd6[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("92e3c75133dc4fdb2cc65f149001b40b - L:378")
# tag::92e3c75133dc4fdb2cc65f149001b40b[]
es.indices.delete(index='customer')
response = es.cat.indices(v=True)
# end::92e3c75133dc4fdb2cc65f149001b40b[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("fa5f618ced25ed2e67a1439bb77ba340 - L:398")
# tag::fa5f618ced25ed2e67a1439bb77ba340[]
response = es.index(
    index='customer',
    id=1,
    body={
        'name': 'John Doe',
    }
)
response = es.get(
    index='customer',
    id=1,
)
es.indices.delete(index='customer')
# end::fa5f618ced25ed2e67a1439bb77ba340[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("21fe98843fe0b5473f515d21803db409 - L:431")
# tag::21fe98843fe0b5473f515d21803db409[]
response = es.index(
    index='customer',
    id=1,
    body={
        'name': 'John Doe',
    }
)
# end::21fe98843fe0b5473f515d21803db409[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("75bda7da7fefff2c16f0423a9aa41c6e - L:442")
# tag::75bda7da7fefff2c16f0423a9aa41c6e[]
response = es.index(
    index='customer',
    id=2,
    body={
        'name': 'Jane Doe',
    }
)
# end::75bda7da7fefff2c16f0423a9aa41c6e[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("37c778346eb67042df5e8edf2485e40a - L:454")
# tag::37c778346eb67042df5e8edf2485e40a[]
response = es.index(
    index='customer',
    body={
        'name': 'Jane Doe',
    }
)
# end::37c778346eb67042df5e8edf2485e40a[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("1c0f3b0bc4b7e53b53755fd3bda5b8cf - L:470")
# tag::1c0f3b0bc4b7e53b53755fd3bda5b8cf[]
response = es.index(
    index='customer',
    body={
        'name': 'Jane Doe',
    }
)
# end::1c0f3b0bc4b7e53b53755fd3bda5b8cf[]
print("---------------------------------------")
print(response)
print("---------------------------------------")


print("6a8d7b34f2b42d5992aaa1ff147062d9 - L:489")
# tag::6a8d7b34f2b42d5992aaa1ff147062d9[]
response = es.update(
    index='customer',
    id=1,
    body={
        'doc': {
            'name': 'Jane Doe',
        },
    },
)
# end::6a8d7b34f2b42d5992aaa1ff147062d9[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("731621af937d66170347b9cc6b4a3c48 - L:501")
# tag::731621af937d66170347b9cc6b4a3c48[]
response = es.update(
    index='customer',
    id=1,
    body={
        'doc': {
            'name': 'Jane Doe',
            'age': 20,
        },
    },
)
# end::731621af937d66170347b9cc6b4a3c48[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("38dfa309717488362d0f784e17ebd1b5 - L:513")
print("TODO")

print("9c5ef83db886840355ff662b6e9ae8ab - L:532")
# tag::9c5ef83db886840355ff662b6e9ae8ab[]
response = es.delete(
    index='customer',
    id=2,
)
# end::9c5ef83db886840355ff662b6e9ae8ab[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("7d32a32357b5ea8819b72608fcc6fd07 - L:550")
# tag::7d32a32357b5ea8819b72608fcc6fd07[]
response = es.bulk(body=[
    {'index': {'_index': 'customer', '_id': 1}},
    {'name': 'John Doe'},
    {'index': {'_index': 'customer', '_id': 2}},
    {'name': 'Jane Doe'},
])
# end::7d32a32357b5ea8819b72608fcc6fd07[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("193864342d9f0a36ec84a91ca325f5ec - L:562")
# tag::193864342d9f0a36ec84a91ca325f5ec[]
response = es.bulk(body=[
    {'index': {'_index': 'customer', '_id': 1}},
    {'name': 'John Doe'},
    {'delete': {'_index': 'customer', '_id': 2}},
])
# end::193864342d9f0a36ec84a91ca325f5ec[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("c181969ef91c3b4a2513c1885be98e26 - L:647")
# tag::c181969ef91c3b4a2513c1885be98e26[]
response = es.search(
    index='bank',
    q='*',
    sort={
        'account_number': 'asc',
    },
)
# end::c181969ef91c3b4a2513c1885be98e26[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("506844befdc5691d835771bcbb1c1a60 - L:720")
# tag::506844befdc5691d835771bcbb1c1a60[]
response = es.search(
    index='bank',
    body={
        'query': {
            'match_all': {},
        },
    },
    sort={
        'account_number': 'asc',
    },
)
# end::506844befdc5691d835771bcbb1c1a60[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("345ea7e9cb5af9e052ce0cf6f1f52c23 - L:789")
# tag::345ea7e9cb5af9e052ce0cf6f1f52c23[]
response = es.search(
    index='bank',
    body={
        'query': {
            'match_all': {},
        },
    },
)
# end::345ea7e9cb5af9e052ce0cf6f1f52c23[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("3d7527bb7ac3b0e1f97b22bdfeb99070 - L:805")
# tag::3d7527bb7ac3b0e1f97b22bdfeb99070[]
response = es.search(
    index='bank',
    body={
        'query': {
            'match_all': {},
        },
    },
    size=1,
)
# end::3d7527bb7ac3b0e1f97b22bdfeb99070[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("3c31f9eb032861bff64abd8b14758991 - L:820")
# tag::3c31f9eb032861bff64abd8b14758991[]
response = es.search(
    index='bank',
    body={
        'query': {
            'match_all': {},
        },
    },
    from_=10,
    size=10,
)
# end::3c31f9eb032861bff64abd8b14758991[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("e8035a7476601ad4b136edb250f92d53 - L:836")
# tag::e8035a7476601ad4b136edb250f92d53[]
response = es.search(
    index='bank',
    body={
        'query': {
            'match_all': {},
        },
    },
    sort={
        'balance': 'desc',
    },
)
# end::e8035a7476601ad4b136edb250f92d53[]
print("---------------------------------------")
print(response)
print("---------------------------------------")

print("b8459547da50aebddbcdd1aaaac02b5f - L:854")
# tag::b8459547da50aebddbcdd1aaaac02b5f[]
response = es.search(
    index='bank',
    body={
        'query': {
            'match_all': {},
        },
    },
    _source=['account_number', 'balance'],
)
# end::b8459547da50aebddbcdd1aaaac02b5f[]
print("---------------------------------------")
print(response)
print("---------------------------------------")
