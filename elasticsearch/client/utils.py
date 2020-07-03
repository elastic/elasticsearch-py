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

from __future__ import unicode_literals

import weakref
from datetime import date, datetime
from functools import wraps
from ..compat import string_types, quote, PY2, unquote, urlparse

# parts of URL to be omitted
SKIP_IN_PATH = (None, "", b"", [], ())


def _normalize_hosts(hosts):
    """
    Helper function to transform hosts argument to
    :class:`~elasticsearch.Elasticsearch` to a list of dicts.
    """
    # if hosts are empty, just defer to defaults down the line
    if hosts is None:
        return [{}]

    # passed in just one string
    if isinstance(hosts, string_types):
        hosts = [hosts]

    out = []
    # normalize hosts to dicts
    for host in hosts:
        if isinstance(host, string_types):
            if "://" not in host:
                host = "//%s" % host

            parsed_url = urlparse(host)
            h = {"host": parsed_url.hostname}

            if parsed_url.port:
                h["port"] = parsed_url.port

            if parsed_url.scheme == "https":
                h["port"] = parsed_url.port or 443
                h["use_ssl"] = True

            if parsed_url.username or parsed_url.password:
                h["http_auth"] = "%s:%s" % (
                    unquote(parsed_url.username),
                    unquote(parsed_url.password),
                )

            if parsed_url.path and parsed_url.path != "/":
                h["url_prefix"] = parsed_url.path

            out.append(h)
        else:
            out.append(host)
    return out


def _escape(value):
    """
    Escape a single value of a URL string or a query parameter. If it is a list
    or tuple, turn it into a comma-separated string first.
    """

    # make sequences into comma-separated stings
    if isinstance(value, (list, tuple)):
        value = ",".join(value)

    # dates and datetimes into isoformat
    elif isinstance(value, (date, datetime)):
        value = value.isoformat()

    # make bools into true/false strings
    elif isinstance(value, bool):
        value = str(value).lower()

    # don't decode bytestrings
    elif isinstance(value, bytes):
        return value

    # encode strings to utf-8
    if isinstance(value, string_types):
        if PY2 and isinstance(value, unicode):  # noqa: F821
            return value.encode("utf-8")
        if not PY2 and isinstance(value, str):
            return value.encode("utf-8")

    return str(value)


def _make_path(*parts):
    """
    Create a URL string from parts, omit all `None` values and empty strings.
    Convert lists and tuples to comma separated values.
    """
    # TODO: maybe only allow some parts to be lists/tuples ?
    return "/" + "/".join(
        # preserve ',' and '*' in url for nicer URLs in logs
        quote(_escape(p), b",*")
        for p in parts
        if p not in SKIP_IN_PATH
    )


# parameters that apply to all methods
GLOBAL_PARAMS = ("pretty", "human", "error_trace", "format", "filter_path")


def query_params(*es_query_params):
    """
    Decorator that pops all accepted parameters from method's kwargs and puts
    them in the params argument.
    """

    def _wrapper(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            params = (kwargs.pop("params", None) or {}).copy()
            headers = {
                k.lower(): v
                for k, v in (kwargs.pop("headers", None) or {}).copy().items()
            }

            if "opaque_id" in kwargs:
                headers["x-opaque-id"] = kwargs.pop("opaque_id")

            for p in es_query_params + GLOBAL_PARAMS:
                if p in kwargs:
                    v = kwargs.pop(p)
                    if v is not None:
                        params[p] = _escape(v)

            # don't treat ignore, request_timeout, and opaque_id as other params to avoid escaping
            for p in ("ignore", "request_timeout"):
                if p in kwargs:
                    params[p] = kwargs.pop(p)
            return func(*args, params=params, headers=headers, **kwargs)

        return _wrapped

    return _wrapper


def _bulk_body(serializer, body):
    # if not passed in a string, serialize items and join by newline
    if not isinstance(body, string_types):
        body = "\n".join(map(serializer.dumps, body))

    # bulk body must end with a newline
    if isinstance(body, bytes):
        if not body.endswith(b"\n"):
            body += b"\n"
    elif isinstance(body, string_types) and not body.endswith("\n"):
        body += "\n"

    return body


class NamespacedClient(object):
    def __init__(self, client):
        self.client = client

    @property
    def transport(self):
        return self.client.transport


class AddonClient(NamespacedClient):
    @classmethod
    def infect_client(cls, client):
        addon = cls(weakref.proxy(client))
        setattr(client, cls.namespace, addon)
        return client
