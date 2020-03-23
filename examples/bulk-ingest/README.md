# Bulk Ingest

A simple script that shows how to ingest a dataset from a file into Elasticsearch.
The file that is used for this example is a `.csv` so each row is turned into a document.

To run this example install the dependencies with `pip`:

```console
python -m pip install -r requirements.txt
```

and then run the script with Python:

```console
python bulk-ingest.py
```

You should see the script downloading the dataset into `nyc-restaurants.csv`

Once all the data is loaded into Elasticsearch you can do queries on the dataset
or create visualizations within Kibana.

```python
import elasticsearch

client = elasticsearch.Elasticsearch()
resp = client.search(
    index="nyc-restaurants",
    size=0,
    body={
        "aggs": {
            "borough": {
                "terms": {
                    "field": "borough"
                },
                "aggs": {
                    "grades": {
                        "terms": {
                            "field": "grade"
                        }
                    }
                }
            }
        }
    }
)
print(resp)
```
