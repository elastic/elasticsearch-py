---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/config.html
---

# Configuration [config]

This page contains information about the most important configuration options of the Python {{es}} client.


## TLS/SSL [tls-and-ssl]

The options in this section can only be used when the node is configured for HTTPS. An error will be raised if using these options with an HTTP node.


### Verifying server certificates [_verifying_server_certificates]

The typical route to verify a cluster certificate is via a "CA bundle" which can be specified via the `ca_certs` parameter. If no options are given and the [certifi package](https://github.com/certifi/python-certifi) is installed then certifi’s CA bundle is used by default.

If you have your own CA bundle to use you can configure via the `ca_certs` parameter:

```python
client = Elasticsearch(
    "https://...",
    ca_certs="/path/to/certs.pem"
)
```

If using a generated certificate or certificate with a known fingerprint you can use the `ssl_assert_fingerprint` to specify the fingerprint which tries to match the server’s leaf certificate during the TLS handshake. If there is any matching certificate the connection is verified, otherwise a `TlsError` is raised.

In Python 3.9 and earlier only the leaf certificate will be verified but in Python 3.10+ private APIs are used to verify any certificate in the certificate chain. This helps when using certificates that are generated on a multi-node cluster.

```python
client = Elasticsearch(
    "https://...",
    ssl_assert_fingerprint=(
        "315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3"
    )
)
```

To disable certificate verification use the `verify_certs=False` parameter. This option should be avoided in production, instead use the other options to verify the clusters' certificate.

```python
client = Elasticsearch(
    "https://...",
    verify_certs=False
)
```


### TLS versions [_tls_versions]

Configuring the minimum TLS version to connect to is done via the `ssl_version` parameter. By default this is set to a minimum value of TLSv1.2. Use the `ssl.TLSVersion` enumeration to specify versions.

```python
import ssl

client = Elasticsearch(
    ...,
    ssl_version=ssl.TLSVersion.TLSv1_2
)
```


### Client TLS certificate authentication [_client_tls_certificate_authentication]

Elasticsearch can be configured to authenticate clients via TLS client certificates. Client certificate and keys can be configured via the `client_cert` and `client_key` parameters:

```python
client = Elasticsearch(
    ...,
    client_cert="/path/to/cert.pem",
    client_key="/path/to/key.pem",
)
```


### Using an SSLContext [_using_an_sslcontext]

For advanced users an `ssl.SSLContext` object can be used for configuring TLS via the `ssl_context` parameter. The `ssl_context` parameter can’t be combined with any other TLS options except for the `ssl_assert_fingerprint` parameter.

```python
import ssl

# Create and configure an SSLContext
ctx = ssl.create_default_context()
ctx.load_verify_locations(...)

client = Elasticsearch(
    ...,
    ssl_context=ctx
)
```


## HTTP compression [compression]

Compression of HTTP request and response bodies can be enabled with the `http_compress` parameter. If enabled then HTTP request bodies will be compressed with `gzip` and HTTP responses will include the `Accept-Encoding: gzip` HTTP header. By default compression is disabled.

```python
client = Elasticsearch(
    ...,
    http_compress=True  # Enable compression!
)
```

HTTP compression is recommended to be enabled when requests are traversing the network. Compression is automatically enabled when connecting to Elastic Cloud.


## Request timeouts [timeouts]

Requests can be configured to timeout if taking too long to be serviced. The `request_timeout` parameter can be passed via the client constructor or the client `.options()` method. When the request times out the node will raise a `ConnectionTimeout` exception which can trigger retries.

Setting `request_timeout` to `None` will disable timeouts.

```python
client = Elasticsearch(
    ...,
    request_timeout=10  # 10 second timeout
)

# Search request will timeout in 5 seconds
client.options(request_timeout=5).search(...)
```


### API and server timeouts [_api_and_server_timeouts]

There are API-level timeouts to take into consideration when making requests which can cause the request to timeout on server-side rather than client-side. You may need to configure both a transport and API level timeout for long running operations.

In the example below there are three different configurable timeouts for the `cluster.health` API all with different meanings for the request:

```python
client.options(
    # Amount of time to wait for an HTTP response to start.
    request_timeout=30
).cluster.health(
    # Amount of time to wait to collect info on all nodes.
    timeout=30,
    # Amount of time to wait for info from the master node.
    master_timeout=10,
)
```


## Retries [retries]

Requests can be retried if they don’t return with a successful response. This provides a way for requests to be resilient against transient failures or overloaded nodes.

The maximum number of retries per request can be configured via the `max_retries` parameter. Setting this parameter to 0 disables retries. This parameter can be set in the client constructor or per-request via the client `.options()` method:

```python
client = Elasticsearch(
    ...,
    max_retries=5
)

# For this API request we disable retries with 'max_retries=0'
client.options(max_retries=0).index(
    index="blogs",
    document={
        "title": "..."
    }
)
```


### Retrying on connection errors and timeouts [_retrying_on_connection_errors_and_timeouts]

Connection errors are automatically retried if retries are enabled. Retrying requests on connection timeouts can be enabled or disabled via the `retry_on_timeout` parameter. This parameter can be set on the client constructor or via the client `.options()` method:

```python
client = Elasticsearch(
    ...,
    retry_on_timeout=True
)
client.options(retry_on_timeout=False).info()
```


### Retrying status codes [_retrying_status_codes]

By default if retries are enabled `retry_on_status` is set to `(429, 502, 503, 504)`. This parameter can be set on the client constructor or via the client `.options()` method. Setting this value to `()` will disable the default behavior.

```python
client = Elasticsearch(
    ...,
    retry_on_status=()
)

# Retry this API on '500 Internal Error' statuses
client.options(retry_on_status=[500]).index(
    index="blogs",
    document={
        "title": "..."
    }
)
```


### Ignoring status codes [_ignoring_status_codes]

By default an `ApiError` exception will be raised for any non-2XX HTTP requests that exhaust retries, if any. If you’re expecting an HTTP error from the API but aren’t interested in raising an exception you can use the `ignore_status` parameter via the client `.options()` method.

A good example where this is useful is setting up or cleaning up resources in a cluster in a robust way:

```python
client = Elasticsearch(...)

# API request is robust against the index not existing:
resp = client.options(ignore_status=404).indices.delete(index="delete-this")
resp.meta.status  # Can be either '2XX' or '404'

# API request is robust against the index already existing:
resp = client.options(ignore_status=[400]).indices.create(
    index="create-this",
    mapping={
        "properties": {"field": {"type": "integer"}}
    }
)
resp.meta.status  # Can be either '2XX' or '400'
```

When using the `ignore_status` parameter the error response will be returned serialized just like a non-error response. In these cases it can be useful to inspect the HTTP status of the response. To do this you can inspect the `resp.meta.status`.


## Sniffing for new nodes [sniffing]

Additional nodes can be discovered by a process called "sniffing" where the client will query the cluster for more nodes that can handle requests.

Sniffing can happen at three different times: on client instantiation, before requests, and on a node failure. These three behaviors can be enabled and disabled with the `sniff_on_start`, `sniff_before_requests`, and `sniff_on_node_failure` parameters.

::::{important}
When using an HTTP load balancer or proxy you cannot use sniffing functionality as the cluster would supply the client with IP addresses to directly connect to the cluster, circumventing the load balancer. Depending on your configuration this might be something you don’t want or break completely.
::::



### Waiting between sniffing attempts [_waiting_between_sniffing_attempts]

To avoid needlessly sniffing too often there is a delay between attempts to discover new nodes. This value can be controlled via the `min_delay_between_sniffing` parameter.


### Filtering nodes which are sniffed [_filtering_nodes_which_are_sniffed]

By default nodes which are marked with only a `master` role will not be used. To change the behavior the parameter `sniffed_node_callback` can be used. To mark a sniffed node not to be added to the node pool return `None` from the `sniffed_node_callback`, otherwise return a `NodeConfig` instance.

```python
from typing import Optional, Dict, Any
from elastic_transport import NodeConfig
from elasticsearch import Elasticsearch

def filter_master_eligible_nodes(
    node_info: Dict[str, Any],
    node_config: NodeConfig
) -> Optional[NodeConfig]:
    # This callback ignores all nodes that are master eligible
    # instead of master-only nodes (default behavior)
    if "master" in node_info.get("roles", ()):
        return None
    return node_config

client = Elasticsearch(
    "https://localhost:9200",
    sniffed_node_callback=filter_master_eligible_nodes
)
```

The `node_info` parameter is part of the response from the `nodes.info()` API, below is an example of what that object looks like:

```json
{
  "name": "SRZpKFZ",
  "transport_address": "127.0.0.1:9300",
  "host": "127.0.0.1",
  "ip": "127.0.0.1",
  "version": "5.0.0",
  "build_hash": "253032b",
  "roles": ["master", "data", "ingest"],
  "http": {
    "bound_address": ["[fe80::1]:9200", "[::1]:9200", "127.0.0.1:9200"],
    "publish_address": "1.1.1.1:123",
    "max_content_length_in_bytes": 104857600
  }
}
```


## Node Pool [node-pool]


### Selecting a node from the pool [_selecting_a_node_from_the_pool]

You can specify a node selector pattern via the `node_selector_class` parameter. The supported values are `round_robin` and `random`. Default is `round_robin`.

```python
client = Elasticsearch(
    ...,
    node_selector_class="round_robin"
)
```

Custom selectors are also supported:

```python
from elastic_transport import NodeSelector

class CustomSelector(NodeSelector):
    def select(nodes): ...

client = Elasticsearch(
    ...,
    node_selector_class=CustomSelector
)
```


### Marking nodes dead and alive [_marking_nodes_dead_and_alive]

Individual nodes of Elasticsearch may have transient connectivity or load issues which may make them unable to service requests. To combat this the pool of nodes will detect when a node isn’t able to service requests due to transport or API errors.

After a node has been timed out it will be moved back to the set of "alive" nodes but only after the node returns a successful response will the node be marked as "alive" in terms of consecutive errors.

The `dead_node_backoff_factor` and `max_dead_node_backoff` parameters can be used to configure how long the node pool will put the node into timeout with each consecutive failure. Both parameters use a unit of seconds.

The calculation is equal to `min(dead_node_backoff_factor * (2 ** (consecutive_failures - 1)), max_dead_node_backoff)`.


## Serializers [serializer]

Serializers transform bytes on the wire into native Python objects and vice-versa. By default the client ships with serializers for `application/json`, `application/x-ndjson`, `text/*`, `application/vnd.apache.arrow.stream` and `application/mapbox-vector-tile`.

You can define custom serializers via the `serializers` parameter:

```python
from elasticsearch import Elasticsearch, JsonSerializer

class JsonSetSerializer(JsonSerializer):
    """Custom JSON serializer that handles Python sets"""
    def default(self, data: Any) -> Any:
        if isinstance(data, set):
            return list(data)
        return super().default(data)

client = Elasticsearch(
    ...,
    # Serializers are a mapping of 'mimetype' to Serializer class.
    serializers={"application/json": JsonSetSerializer()}
)
```

If the `orjson` package is installed, you can use the faster ``OrjsonSerializer`` for the default mimetype (``application/json``):

```python
from elasticsearch import Elasticsearch, OrjsonSerializer

es = Elasticsearch(
    ...,
    serializer=OrjsonSerializer()
)
```

orjson is particularly fast when serializing vectors as it has native numpy support. This will be the default in a future release. Note that you can install orjson with the `orjson` extra:

```sh
$ python -m pip install elasticsearch[orjson]
```


## Nodes [nodes]


### Node implementations [_node_implementations]

The default node class for synchronous I/O is `urllib3` and the default node class for asynchronous I/O is `aiohttp`.

For all of the built-in HTTP node implementations like `urllib3`, `requests`, and `aiohttp` you can specify with a simple string to the `node_class` parameter:

```python
from elasticsearch import Elasticsearch

client = Elasticsearch(
    ...,
    node_class="requests"
)
```

You can also specify a custom node implementation via the `node_class` parameter:

```python
from elasticsearch import Elasticsearch
from elastic_transport import Urllib3HttpNode

class CustomHttpNode(Urllib3HttpNode):
    ...

client = Elasticsearch(
    ...
    node_class=CustomHttpNode
)
```


### HTTP connections per node [_http_connections_per_node]

Each node contains its own pool of HTTP connections to allow for concurrent requests. This value is configurable via the `connections_per_node` parameter:

```python
client = Elasticsearch(
    ...,
    connections_per_node=5
)
```

