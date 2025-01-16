# CI certificates

This directory contains certificates that can be used to test against Elasticsearch in CI

## Generating new certificates using the Certificate Authority cert and key

Before adding support for Python 3.13, we generated certificates with
[`elasticsearch-certutil`](https://www.elastic.co/guide/en/elasticsearch/reference/current/certutil.html).
However, those certificates are not compliant with RFC 5280, and Python now
enforces compliance by enabling the VERIFY_X509_STRICT flag by default.

If you need to generate new certificates, you can do so with
[trustme](https://trustme.readthedocs.io/en/latest/) as follows:

```
```bash
pip install trustme
python -m trustme --identities instance
# Use the filenames expected by our tests
mv client.pem ca.crt
mv server.pem testnode.crt
mv server.key testnode.key
```

For more control over the generated certificates, trustme also offers a Python
API, but we have not needed it so far.
