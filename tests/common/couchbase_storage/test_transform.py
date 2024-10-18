from datetime import UTC, datetime, timedelta
import time
from unittest.mock import patch, MagicMock
import pytest

from vulsy.common.couchbase_storage.exceptions import DocumentRetrievalError
from vulsy.common.couchbase_storage.repo import generic
from vulsy.common.couchbase_storage.repo.ingestion import IngestionDataRepositoryImpl
from vulsy.common.couchbase_storage.repo.transform import _TRANSFORMATION_META_KEY, TransformationDataRepositoryImpl
from vulsy.common.simpel import now
from vulsy.vulnerability_pipeline.ingestion.models import EndpointRawDataEvent
from vulsy.vulnerability_pipeline.transformation.models import EndpointMetadata, TransformationMetadata


@pytest.fixture
def repo():
    """Create an instance of TransformationDataRepositoryImpl."""
    return TransformationDataRepositoryImpl()


@pytest.fixture
def mock_generic():
    """Mock the generic module."""
    with patch("vulsy.common.couchbase_storage.repo.transform.generic") as mock:
        yield mock


def test_get_transformation_metadata(repo, mock_generic):
    expected = TransformationMetadata(last_queued_timestamp=now())
    mock_generic.get.return_value = expected

    result = repo.get_transformation_metadata()

    mock_generic.get.assert_called_once_with(
        _TRANSFORMATION_META_KEY,
        TransformationMetadata,
        repo.meta_collection_getter,
    )
    assert result == expected


@pytest.mark.database
def test_get_next_ingestion_event(repo):
    timestamp_now = now()
    event_one = EndpointRawDataEvent(
        name="NVD",
        hash="test_hash",
        url="https://nvd.nist.gov/vuln/detail/CVE-2024-0001",
        data="one",
        timestamp=(datetime.now(UTC) + timedelta(minutes=1)).isoformat(),
    )
    event_two = EndpointRawDataEvent(
        name="NVD",
        hash="test_hash_two",
        url="https://nvd.nist.gov/vuln/detail/CVE-2024-0002",
        data="two",
        timestamp=(datetime.now(UTC) + timedelta(minutes=2)).isoformat(),
    )
    ingestion = IngestionDataRepositoryImpl()
    ingestion.store_event(event_one)
    ingestion.store_event(event_two)

    id, result = repo.get_next_ingestion_event(timestamp_now)
    assert id == "NVD:test_hash"
    assert result.timestamp == event_one.timestamp
    assert result.hash == event_one.hash


def test_get_next_ingestion_event_none(repo):
    """Test get_next_ingestion_event when no events are found."""
    with patch("vulsy.common.couchbase_storage.repo.transform.get_cluster") as mock_cluster:
        mock_result = MagicMock()
        mock_result.rows.return_value = []
        mock_cluster.return_value.query.return_value = mock_result

        result = repo.get_next_ingestion_event("2024-01-01T00:00:00+00:00")

        assert result is None
        mock_cluster.return_value.query.assert_called_once()


def test_get_transformation_metadata_not_found(repo, mock_generic):
    """Test get_transformation_metadata when metadata is not found initially."""
    mock_generic.get.side_effect = [None, TransformationMetadata(last_queued_timestamp="2024-01-01T00:00:00+00:00")]

    result = repo.get_transformation_metadata()

    assert isinstance(result, TransformationMetadata)
    assert mock_generic.get.call_count == 2
    mock_generic.upsert.assert_called_once()


def test_get_transformation_metadata_error(repo, mock_generic):
    """Test get_transformation_metadata when metadata is not found after upsert."""
    mock_generic.get.return_value = None

    with pytest.raises(DocumentRetrievalError, match="Transformation metadata not found"):
        repo.get_transformation_metadata()


def test_find_endpoint_metadata(repo, mock_generic):
    """Test find_endpoint_metadata."""
    expected = EndpointMetadata(url="https://example.com", events=[], timestamp="2024-01-01T00:00:00+00:00")
    mock_generic.get.return_value = expected

    result = repo.find_endpoint_metadata("test_key")

    assert result == expected
    mock_generic.get.assert_called_once_with("test_key", EndpointMetadata, repo.meta_collection_getter)


@pytest.mark.database
def test_store_new_metadata(repo):
    """Test store_new_metadata with database."""
    meta = TransformationMetadata(last_queued_timestamp="2024-01-01T00:00:00+00:00")
    generic.upsert(_TRANSFORMATION_META_KEY, meta.model_dump(), repo.meta_collection_getter)
    endpoint_meta = EndpointMetadata(
        url="https://example-store-new-metadata.com", events=[], timestamp="2024-01-01T00:00:00+00:00"
    )

    repo.store_new_metadata(meta, endpoint_meta)

    # Verify the data was stored
    assert repo.get_transformation_metadata() is not None
    assert repo.find_endpoint_metadata(f"ENDPOINT:{endpoint_meta.url_as_hash()}") is not None
    pass


@pytest.mark.database
def test_replace_existing_metadata(repo):
    """Test replace_existing_metadata with database."""
    # First store initial data
    meta = TransformationMetadata(last_queued_timestamp="2024-01-01T00:00:00+00:00")
    generic.upsert(_TRANSFORMATION_META_KEY, meta.model_dump(), repo.meta_collection_getter)
    initial_endpoint = EndpointMetadata(
        url="https://example-existing.com", events=[], timestamp="2024-01-01T00:00:00+00:00"
    )
    repo.store_new_metadata(meta, initial_endpoint)

    # Now replace with new data
    new_meta = TransformationMetadata(last_queued_timestamp="2024-01-02T00:00:00+00:00")
    new_endpoint = EndpointMetadata(
        url="https://example-existing.com", events=[], timestamp="2024-01-02T00:00:00+00:00"
    )

    repo.replace_existing_metadata(new_meta, new_endpoint)

    # Verify the data was updated
    stored_endpoint = repo.find_endpoint_metadata(f"ENDPOINT:{new_endpoint.url_as_hash()}")

    assert repo.get_transformation_metadata().last_queued_timestamp == new_meta.last_queued_timestamp
    assert stored_endpoint.timestamp == new_endpoint.timestamp


@pytest.mark.database
def test_get_next_endpoint_to_transform(repo):
    """Test get_next_endpoint_to_transform with database."""
    # Create and store test endpoint metadata
    endpoint = EndpointMetadata(
        url="https://example.com/test",
        events=[
            {
                "status": "unprocessed",
                "timestamp": now(),
                "event_id": "1",
                "original_event_timestamp": "2024-01-01T00:00:00+00:00",
            }
        ],
        timestamp=now(),
    )
    meta = TransformationMetadata(last_queued_timestamp=now())
    generic.upsert(_TRANSFORMATION_META_KEY, meta.model_dump(), repo.meta_collection_getter)
    repo.store_new_metadata(meta, endpoint)

    # Get next endpoint to transform
    cb_endpoint = repo.get_next_endpoint_to_transform()
    assert cb_endpoint is not None

    doc_id, endpoint_data = cb_endpoint
    assert doc_id == f"ENDPOINT:{endpoint.url_as_hash()}"
    assert endpoint_data.url == endpoint.url
    assert endpoint_data.events[0].status == "unprocessed"


def test_get_next_endpoint_to_transform_none(repo):
    """Test get_next_endpoint_to_transform when no endpoints are found."""
    with patch("vulsy.common.couchbase_storage.repo.transform.get_cluster") as mock_cluster:
        mock_result = MagicMock()
        mock_result.rows.return_value = []
        mock_cluster.return_value.query.return_value = mock_result

        result = repo.get_next_endpoint_to_transform()

        assert result is None
        mock_cluster.return_value.query.assert_called_once()


@pytest.mark.database
def test_get_next_endpoint_to_transform_retry_status(repo):
    """Test get_next_endpoint_to_transform with retry status."""
    # Create and store test endpoint metadata with retry status
    endpoint = EndpointMetadata(
        url="https://example.com/retry-test",
        events=[
            {
                "status": "retry",
                "timestamp": now(),
                "event_id": "2",
                "original_event_timestamp": "2024-01-01T00:00:00+00:00",
            }
        ],
        timestamp=now(),
    )
    meta = TransformationMetadata(last_queued_timestamp=now())
    generic.upsert(_TRANSFORMATION_META_KEY, meta.model_dump(), repo.meta_collection_getter)
    repo.store_new_metadata(meta, endpoint)

    # Get next endpoint to transform
    cb_endpoint = repo.get_next_endpoint_to_transform()
    assert cb_endpoint is not None

    doc_id, endpoint_data = cb_endpoint
    assert doc_id == f"ENDPOINT:{endpoint.url_as_hash()}"
    assert endpoint_data.url == endpoint.url
    assert endpoint_data.events[0].status == "retry"
