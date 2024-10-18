"""Couchbase server configuration."""

import logging

from couchbase.exceptions import (
    BucketAlreadyExistsException,
    CollectionAlreadyExistsException,
    ScopeAlreadyExistsException,
)
from couchbase.management.buckets import CreateBucketSettings

from vulsy.common.couchbase_storage.server import couchbase_config, get_cluster

logger = logging.getLogger(__name__)


def configure() -> None:
    """Configure Couchbase server with the necessary buckets, scopes, and collections.

    https://docs.couchbase.com/cloud/clusters/data-service/about-buckets-scopes-collections.html
    """
    for scope in couchbase_config.scopes:
        for collection in scope.collections:
            _configure(couchbase_config.bucket, scope.name, collection)


def _configure(
    bucket_name: str,
    scope_name: str,
    collection_name: str,
    bucket_ram_quota_mb: int = 100,
) -> None:
    """Configure Couchbase server with a bucket, scope, and collection.

    This function connects to a Couchbase server and creates a bucket, scope, and collection
    if they don't already exist.

    Args:
        connection_string: The connection string for the Couchbase cluster.
        username: The username for authentication.
        password: The password for authentication.
        bucket_name: The name of the bucket to create or use.
        scope_name: The name of the scope to create or use.
        collection_name: The name of the collection to create or use.
        bucket_ram_quota_mb: The RAM quota for the bucket in MB. Defaults to 100 MB.

    Raises:
        Exception: If there's an error connecting to the cluster or performing operations.
    """
    cluster = get_cluster()

    # Get a reference to the bucket manager
    bucket_manager = cluster.buckets()

    # Check if the bucket exists, create it if it doesn't
    try:
        bucket_manager.create_bucket(
            CreateBucketSettings(name=bucket_name, ram_quota_mb=bucket_ram_quota_mb, flush_enabled=True)
        )
        logger.info("Bucket '%s' created successfully.", bucket_name)
    except BucketAlreadyExistsException:
        logger.info("Bucket '%s' already exists.", bucket_name)

    # Get a reference to the bucket
    bucket = cluster.bucket(bucket_name)

    # Get a reference to the collection manager
    collection_manager = bucket.collections()

    # Check if the scope exists, create it if it doesn't
    try:
        collection_manager.create_scope(scope_name)
        logger.info("Scope '%s' created successfully.", scope_name)
    except ScopeAlreadyExistsException:
        logger.info("Scope '%s' already exists.", scope_name)

    # Check if the collection exists, create it if it doesn't
    try:
        collection_manager.create_collection(scope_name, collection_name)
        logger.info("Collection '%s' created successfully.", collection_name)
    except CollectionAlreadyExistsException:
        logger.info("Collection '%s' already exists.", collection_name)

    logger.info("Couchbase server configuration completed successfully.")
