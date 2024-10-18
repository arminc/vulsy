"""Ingestion data repository implementation."""

from functools import partial

from couchbase.options import QueryOptions

from vulsy.common.couchbase_storage.exceptions import DocumentRetrievalError
from vulsy.common.couchbase_storage.repo import generic
from vulsy.common.couchbase_storage.server import couchbase_config, get_cluster
from vulsy.common.simpel import epoch_start
from vulsy.vulnerability_pipeline.ingestion.models import EndpointRawDataEvent
from vulsy.vulnerability_pipeline.transformation.models import (
    EndpointMetadata,
    TransformationMetadata,
)
from vulsy.vulnerability_pipeline.transformation.transform import TransformationDataRepository

_TRANSFORMATION_META_KEY = "TRANSFORMATION:last"


class TransformationDataRepositoryImpl(TransformationDataRepository):
    """Transformation data repository implementation for Couchbase."""

    meta_collection_getter = partial(
        generic.get_collection,
        collection_name=couchbase_config.transformation.meta,
        scope_name=couchbase_config.transformation.name,
        bucket_name=couchbase_config.bucket,
    )

    def get_next_ingestion_event(self, last_timestamp: str) -> tuple[str, EndpointRawDataEvent] | None:
        """Get the source item events.

        Args:
            last_timestamp: The last timestamp.

        Returns:
            Tuple of (document_key, event_data) if found, None otherwise.
        """
        query = """
                SELECT META().id as doc_id, e.*
                FROM vulsy.ingestion.events as e
                WHERE e.timestamp > $last_timestamp
                ORDER BY e.timestamp ASC
                LIMIT 1;
                """
        result = get_cluster().query(query, QueryOptions(named_parameters={"last_timestamp": last_timestamp}))
        for row in result.rows():
            doc_id = row["doc_id"]
            return doc_id, EndpointRawDataEvent.model_validate(row)
        return None

    def get_transformation_metadata(self) -> TransformationMetadata:
        """Get the transformation metadata."""
        meta = generic.get(_TRANSFORMATION_META_KEY, TransformationMetadata, self.meta_collection_getter)
        if meta is None:
            generic.upsert(
                _TRANSFORMATION_META_KEY,
                TransformationMetadata(last_queued_timestamp=epoch_start()).model_dump(),
                self.meta_collection_getter,
            )
            meta = generic.get(_TRANSFORMATION_META_KEY, TransformationMetadata, self.meta_collection_getter)
            if meta is None:
                raise DocumentRetrievalError("Transformation metadata not found")
        return meta

    def find_endpoint_metadata(self, key: str) -> EndpointMetadata | None:
        """Find the transformation metadata for a specific source item.

        Returns:
            Transformation metadata.
        """
        return generic.get(key, EndpointMetadata, self.meta_collection_getter)

    def store_new_metadata(self, meta: TransformationMetadata, endpoint_meta: EndpointMetadata) -> None:
        """Store the endpoint metadata.

        Args:
            meta: Transformation metadata.
            endpoint_meta: Endpoint metadata.
        """
        get_cluster().transactions.run(
            lambda ctx: (
                collection := self.meta_collection_getter(get_cluster()),
                ctx.replace(ctx.get(collection, _TRANSFORMATION_META_KEY), meta.model_dump()),
                ctx.insert(collection, f"ENDPOINT:{endpoint_meta.url_as_hash()}", endpoint_meta.model_dump()),
            )
        )

    def replace_existing_metadata(self, meta: TransformationMetadata, endpoint_meta: EndpointMetadata) -> None:
        """Replace the existing transformation metadata and endpoint metadata.

        Args:
            meta: Transformation metadata.
            endpoint_meta: Endpoint metadata.
        """
        get_cluster().transactions.run(
            lambda ctx: (
                collection := self.meta_collection_getter(get_cluster()),
                ctx.replace(ctx.get(collection, _TRANSFORMATION_META_KEY), meta.model_dump()),
                ctx.replace(ctx.get(collection, f"ENDPOINT:{endpoint_meta.url_as_hash()}"), endpoint_meta.model_dump()),
            )
        )

    def get_next_endpoint_to_transform(self) -> tuple[str, EndpointMetadata] | None:
        """Get the next endpoint to transform."""
        query = """
                SELECT META().id as doc_id, e.*
                FROM vulsy.transformation.meta AS e
                WHERE ANY event IN e.events
                    SATISFIES event.status IN ["unprocessed", "retry"] END
                ORDER BY e.timestamp DESC
                LIMIT 1;
                """
        result = get_cluster().query(query)
        for row in result.rows():
            doc_id = row["doc_id"]
            return doc_id, EndpointMetadata.model_validate(row)
        return None
