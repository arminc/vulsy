from functools import partial
import time
from pydantic import BaseModel
import pytest

from vulsy.common.couchbase_storage.repo import generic
from vulsy.common.couchbase_storage.server import couchbase_config


class TestData(BaseModel):
    test: str = "abcd"


@pytest.mark.database
def test_database_query():
    collection_getter = partial(
        generic.get_collection,
        collection_name=couchbase_config.ingestion.meta,
        scope_name=couchbase_config.ingestion.name,
        bucket_name=couchbase_config.bucket,
    )
    generic.upsert("test", TestData().model_dump(), collection_getter)
    data = generic.get("test", TestData, collection_getter)
    assert data is not None
    assert data.test == "abcd"
