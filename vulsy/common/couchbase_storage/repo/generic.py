"""Generic functions for interacting with Couchbase."""

from collections.abc import Callable
from typing import TypeVar

from couchbase.cluster import Cluster
from couchbase.collection import Collection
from couchbase.exceptions import DocumentNotFoundException
from pydantic import BaseModel

from vulsy.common.couchbase_storage.exceptions import DocumentRetrievalError, DocumentStorageError
from vulsy.common.couchbase_storage.server import get_cluster

T = TypeVar("T", bound=BaseModel)


def get_collection(cluster: Cluster, collection_name: str, scope_name: str, bucket_name: str) -> Collection:
    """Get a collection from the cluster.

    Args:
        cluster: The cluster to get the collection from.
        collection_name: The name of the collection.
        scope_name: The name of the scope.
        bucket_name: The name of the bucket.
    """
    return cluster.bucket(bucket_name).scope(scope_name).collection(collection_name)


def get(key: str, model_type: type[T], collection: Callable[[Cluster], Collection]) -> T | None:
    """Get a document from the cluster.

    Args:
        key: The key of the document to get.
        model_type: The type of the document to get.
        collection: The collection to get the document from.

    Returns:
        The document if found, otherwise None.

    Raises:
        DocumentRetrievalError: If there is an error retrieving the document.
    """
    try:
        result = collection(get_cluster()).get(key)
        data = result.content_as[dict]
        return model_type.model_validate(data)
    except DocumentNotFoundException:
        return None
    except Exception as e:
        raise DocumentRetrievalError("Error retrieving document") from e


def upsert(key: str, data: dict, collection: Callable[[Cluster], Collection]) -> None:
    """Upsert a document to the cluster.

    Args:
        key: The key of the document to upsert.
        data: The data of the document to upsert.
        collection: The collection to upsert the document to.

    Raises:
        DocumentStorageError: If there is an error storing the document.
    """
    try:
        collection(get_cluster()).upsert(key, data)
    except Exception as e:
        raise DocumentStorageError("Error storing document") from e
