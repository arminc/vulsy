"""Couchbase server configuration."""

from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from pydantic import BaseModel

from vulsy.settings import settings

_cluster: Cluster | None = None


class ScopeConfig(BaseModel):
    """Configuration for a Couchbase scope.

    Attributes:
        name: The name of the scope.
        collections: A list of collection names within the scope.
    """

    name: str
    collections: list[str]


class IngestionConfig(ScopeConfig):
    """Configuration for the data ingestion scope.

    Attributes:
        name: The name of the scope, defaulting to "ingestion".
        events: The name of the ingestion events collection, defaulting to "events".
        meta: The name of the ingestion meta collection, defaulting to "meta".
        metrics: The name of the metrics collection, defaulting to "metrics".
        collections: A list of collection names, defaulting to [events, meta, metrics].
    """

    name: str = "ingestion"
    meta: str = "meta"
    events: str = "events"
    metrics: str = "metrics"

    collections: list[str] = [events, meta, metrics]


class TransformationConfig(ScopeConfig):
    """Configuration for the data transformation scope.

    Attributes:
        name: The name of the scope, defaulting to "transformation".
        meta: The name of the transformation meta collection, defaulting to "meta".
        events: The name of the transformation events collection, defaulting to "events".
        metrics: The name of the metrics collection, defaulting to "metrics".
        collections: A list of collection names, defaulting to [events, meta, metrics].
    """

    name: str = "transformation"
    meta: str = "meta"
    events: str = "events"
    metrics: str = "metrics"

    collections: list[str] = [events, meta, metrics]


class CouchbaseConfig(BaseModel):
    """Configuration for the Couchbase connection.

    Attributes:
        bucket: The name of the Couchbase bucket, defaulting to "vulsy".
        data_ingestion: Configuration for the data ingestion scope.
        scopes: A list of scope configurations.
    """

    bucket: str = "vulsy"
    ingestion: IngestionConfig = IngestionConfig()
    transformation: TransformationConfig = TransformationConfig()

    scopes: list[ScopeConfig] = [ingestion, transformation]


couchbase_config: CouchbaseConfig = CouchbaseConfig()


def _initialize_cluster() -> None:
    """Initialize the Couchbase cluster.

    This function should be called once at application startup.
    """
    global _cluster
    if _cluster is None:
        auth = PasswordAuthenticator(settings.couchbase.username, settings.couchbase.password.get_secret_value())
        _cluster = Cluster(settings.couchbase.url, ClusterOptions(auth))


def get_cluster() -> Cluster:
    """Get the Couchbase cluster instance.

    Returns:
        Cluster: The initialized Couchbase cluster.

    Raises:
        RuntimeError: If the cluster has not been initialized.
    """
    _initialize_cluster()
    if _cluster is None:
        raise RuntimeError("Couchbase cluster has not been initialized. Call initialize_cluster() first.")
    return _cluster
