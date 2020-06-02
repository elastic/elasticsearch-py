# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

import random
import urllib3
import time


endpoints = [
    "http://app:9292/",
    "http://app:9292/ingest",
    "http://app:9292/search/mario",
    "http://app:9292/search/sonic",
    "http://app:9292/search/donkeykong",
    "http://app:9292/search/bubsy",
    "http://app:9292/delete",
    "http://app:9292/update",
    "http://app:9292/error",
]


def main():
    http = urllib3.PoolManager()
    while True:
        url = random.choice(endpoints)
        try:
            http.request("GET", url, preload_content=True)
        except Exception:
            pass
        time.sleep(1)


main()
