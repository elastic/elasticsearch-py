from ..utils import NamespacedClient, query_params

from .ccr import CcrClient
from .data_frame import Data_FrameClient
from .deprecation import DeprecationClient
from .graph import GraphClient
from .ilm import IlmClient
from ..indices import IndicesClient
from .license import LicenseClient
from .migration import MigrationClient
from .ml import MlClient
from .monitoring import MonitoringClient
from .rollup import RollupClient
from .security import SecurityClient
from .sql import SqlClient
from .ssl import SslClient
from .watcher import WatcherClient

XPACK_NAMESPACES = {
    "ccr": CcrClient,
    "data_frame": Data_FrameClient,
    "deprecation": DeprecationClient,
    "graph": GraphClient,
    "ilm": IlmClient,
    "indices": IndicesClient,
    "license": LicenseClient,
    "migration": MigrationClient,
    "ml": MlClient,
    "monitoring": MonitoringClient,
    "rollup": RollupClient,
    "security": SecurityClient,
    "sql": SqlClient,
    "ssl": SslClient,
    "watcher": WatcherClient,
}

class XPackClient(NamespacedClient):
    def __init__(self, *args, **kwargs):
        super(XPackClient, self).__init__(*args, **kwargs)

        for namespace in XPACK_NAMESPACES:
            setattr(self, namespace, getattr(self.client, namespace))

    @query_params("categories", "human")
    def info(self, params=None):
        """
        Retrieve information about xpack, including build number/timestamp and license status
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/info-api.html>`_

        :arg categories: Comma-separated list of info categories. Can be any of:
            build, license, features
        :arg human: Presents additional info for humans (feature descriptions
            and X-Pack tagline)
        """
        return self.transport.perform_request("GET", "/_xpack", params=params)

    @query_params("master_timeout")
    def usage(self, params=None):
        """
        Retrieve information about xpack features usage

        :arg master_timeout: Specify timeout for watch write operation
        """
        return self.transport.perform_request("GET", "/_xpack/usage", params=params)
