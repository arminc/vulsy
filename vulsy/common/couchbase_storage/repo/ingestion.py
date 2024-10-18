"""Ingestion data repository implementation."""

from functools import partial

from vulsy.common.couchbase_storage.repo import generic
from vulsy.common.couchbase_storage.server import couchbase_config
from vulsy.vulnerability_pipeline.ingestion.ingest import IngestionDataRepository
from vulsy.vulnerability_pipeline.ingestion.models import EndpointRawDataEvent, Metrics, SourceIngestionMetadata


class IngestionDataRepositoryImpl(IngestionDataRepository):
    """Ingestion data repository implementation for Couchbase."""

    data_ingestion_meta_collection_getter = partial(
        generic.get_collection,
        collection_name=couchbase_config.ingestion.meta,
        scope_name=couchbase_config.ingestion.name,
        bucket_name=couchbase_config.bucket,
    )

    data_ingestion_collection_getter = partial(
        generic.get_collection,
        collection_name=couchbase_config.ingestion.events,
        scope_name=couchbase_config.ingestion.name,
        bucket_name=couchbase_config.bucket,
    )

    data_ingestion_metrics_collection_getter = partial(
        generic.get_collection,
        collection_name=couchbase_config.ingestion.metrics,
        scope_name=couchbase_config.ingestion.name,
        bucket_name=couchbase_config.bucket,
    )

    def get_source_metadata(self, key: str) -> SourceIngestionMetadata | None:
        """Retrieve a document from Couchbase by key.

        Args:
            key: The key of the document to retrieve.

        Returns:
            The document if found, otherwise None.

        Raises:
            DocumentRetrievalError: If there is an error retrieving the document.
        """
        return generic.get(key, SourceIngestionMetadata, self.data_ingestion_meta_collection_getter)

    def store_source_metadata(self, key: str, metadata: SourceIngestionMetadata) -> None:
        """Store a SourceIngestMetadata document in Couchbase by key.

        Args:
            key: The key under which the document will be stored.
            metadata: The SourceIngestMetadata object to store.

        Raises:
            DocumentStorageError: If there is an error storing the document.
        """
        return generic.upsert(key, metadata.model_dump(), self.data_ingestion_meta_collection_getter)

    def find_event(self, source_name: str, hash_value: str) -> EndpointRawDataEvent | None:
        """Retrieve a SourceItemEvent document from Couchbase by source name and hash.

        Args:
            source_name: The name of the source.
            hash_value: The hash of the event to retrieve.

        Returns:
            The SourceItemEvent document if found, otherwise None.

        Raises:
            DocumentRetrievalError: If there is an error retrieving the document.
        """
        key = f"{source_name}:{hash_value}"
        return generic.get(key, EndpointRawDataEvent, self.data_ingestion_collection_getter)

    def store_event(self, event: EndpointRawDataEvent) -> None:
        """Store a SourceItemEvent document in Couchbase.

        Args:
            event: The SourceItemEvent object to store.

        Raises:
            DocumentStorageError: If there is an error storing the document.
        """
        key = f"{event.name}:{event.hash}"
        generic.upsert(key, event.model_dump(), self.data_ingestion_collection_getter)

    def get_metrics(self, source_name: str, date: str) -> Metrics | None:
        """Retrieve metrics for a specific source and date.

        Args:
            source_name: The name of the source.
            date: The date for which to retrieve metrics.

        Returns:
            The Metrics object if found, otherwise None.
        """
        key = f"{source_name}:{date}"
        return generic.get(key, Metrics, self.data_ingestion_metrics_collection_getter)

    def store_metrics(self, metrics: Metrics) -> None:
        """Store metrics in Couchbase.

        Args:
            metrics: The Metrics object to store.

        Raises:
            DocumentStorageError: If there is an error storing the document.
        """
        key = f"{metrics.source_name}:{metrics.day}"
        generic.upsert(key, metrics.model_dump(), self.data_ingestion_metrics_collection_getter)
