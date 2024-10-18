from unittest.mock import Mock, patch

import pytest

from vulsy.common.couchbase_storage.repo.ingestion import IngestionDataRepositoryImpl
from vulsy.vulnerability_pipeline.ingestion.models import SourceIngestionMetadata, EndpointRawDataEvent, Metrics


@pytest.fixture
def repo():
    """Create an instance of IngestionDataRepositoryImpl."""
    return IngestionDataRepositoryImpl()


@pytest.fixture
def mock_generic():
    """Mock the generic module."""
    with patch("vulsy.common.couchbase_storage.repo.ingestion.generic") as mock:
        yield mock


def test_get_source_metadata(repo, mock_generic):
    """Test retrieving source metadata."""
    expected = SourceIngestionMetadata(last_run="2024-01-01")
    mock_generic.get.return_value = expected

    result = repo.get_source_metadata("test_key")

    mock_generic.get.assert_called_once_with(
        "test_key",
        SourceIngestionMetadata,
        repo.data_ingestion_meta_collection_getter,
    )
    assert result == expected


def test_store_source_metadata(repo, mock_generic):
    """Test storing source metadata."""
    metadata = SourceIngestionMetadata(last_run="2024-01-01")

    repo.store_source_metadata("test_key", metadata)

    mock_generic.upsert.assert_called_once_with(
        "test_key",
        metadata.model_dump(),
        repo.data_ingestion_meta_collection_getter,
    )


def test_find_event(repo, mock_generic):
    """Test finding an event."""
    expected = EndpointRawDataEvent(
        name="NVD",
        hash="test_hash",
        url="https://nvd.nist.gov/vuln/detail/CVE-2024-0001",
        data="",
    )
    mock_generic.get.return_value = expected

    result = repo.find_event("NVD", "test_hash")

    mock_generic.get.assert_called_once_with(
        "NVD:test_hash",
        EndpointRawDataEvent,
        repo.data_ingestion_collection_getter,
    )
    assert result == expected


def test_store_event(repo, mock_generic):
    """Test storing an event."""
    event = EndpointRawDataEvent(
        name="NVD",
        hash="test_hash",
        url="https://nvd.nist.gov/vuln/detail/CVE-2024-0001",
        data="",
    )

    repo.store_event(event)

    mock_generic.upsert.assert_called_once_with(
        "NVD:test_hash",
        event.model_dump(),
        repo.data_ingestion_collection_getter,
    )


def test_get_metrics(repo, mock_generic):
    """Test retrieving metrics."""
    expected = Metrics(
        source_name="NVD",
        day="01-01-2024",
        ts_start=1715548800000,
        ts_end=1715548800000,
        ts_data=[],
    )
    mock_generic.get.return_value = expected

    result = repo.get_metrics("NVD", "01-01-2024")

    mock_generic.get.assert_called_once_with(
        "NVD:01-01-2024",
        Metrics,
        repo.data_ingestion_metrics_collection_getter,
    )
    assert result == expected


def test_store_metrics(repo, mock_generic):
    """Test storing metrics."""
    metrics = Metrics(
        source_name="NVD",
        day="01-01-2024",
        ts_start=1715548800000,
        ts_end=1715548800000,
        ts_data=[],
    )

    repo.store_metrics(metrics)

    mock_generic.upsert.assert_called_once_with(
        "NVD:01-01-2024",
        metrics.model_dump(),
        repo.data_ingestion_metrics_collection_getter,
    )
