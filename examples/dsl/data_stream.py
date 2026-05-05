import os
from datetime import datetime
from typing import Any, Dict, Generator

from elasticsearch import dsl
from elasticsearch.dsl import types


class Log(dsl.Document):
    timestamp: dsl.M[datetime] = dsl.mapped_field(
        dsl.Date(default_timezone="UTC"), es_name="@timestamp"
    )
    level: dsl.M[str] = dsl.mapped_field(dsl.Keyword())
    message: dsl.M[str]

    class Index:
        name = "logs"
        data_stream = True
        # pass a desired index lifecycle policy as follows:
        # settings = {'index': {'lifecycle': {'name': 'my-ilm'}}}


def main() -> None:
    # initiate the default connection to elasticsearch
    client = dsl.connections.create_connection(hosts=[os.environ["ELASTICSEARCH_URL"]])

    # delete a previous instance of the data stream if one exists
    if Log._index.exists():
        Log._index.delete()

    # create the data stream
    Log.init()

    # write an individual entry
    message = Log(
        timestamp=datetime(2026, 1, 1, 0, 30, 22),
        level="error",
        message="test error (individual)",
    )
    message.save()

    # write multiple entries using the bulk API
    def get_next_log() -> Generator[Dict[str, Any]]:
        yield {
            "_source": Log(
                timestamp=datetime(2026, 1, 1, 10, 30, 45),
                level="warning",
                message="test warning",
            ),
            "_op_type": "create",
        }
        yield {
            "_source": Log(
                timestamp=datetime(2026, 1, 1, 10, 30, 46),
                level="critical",
                message="test error (bulk)",
            ),
            "_op_type": "create",
        }
        yield {
            "_source": Log(
                timestamp=datetime(2026, 1, 1, 10, 30, 50),
                level="info",
                message="test info message",
            ),
            "_op_type": "create",
        }

    Log.bulk(get_next_log(), refresh=True)

    # search the data stream
    match_query = Log.search().query(
        dsl.query.Match("message", types.MatchQuery(query="error"))
    )
    for log in match_query:
        print(f"{log.meta.id} {log.timestamp.isoformat()} [{log.level}] {log.message}")

    # close the connection
    dsl.connections.get_connection().close()


if __name__ == "__main__":
    main()
