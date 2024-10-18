import pytest
from regex import F
from vulsy.common.couchbase_storage.server import get_cluster, couchbase_config


@pytest.fixture(scope="function", autouse=True)
def clear_couchbase_db(request):
    # Check if the test is marked with @pytest.mark.database
    if "database" in request.keywords:
        # Configure your cluster connection
        bucket = get_cluster().bucket(couchbase_config.bucket)

        for scope in couchbase_config.scopes:
            for collection in scope.collections:
                cb_collection = bucket.scope(scope.name).collection(collection)

                # Clear all documents from the current collection
                query = f"SELECT META().id FROM `{couchbase_config.bucket}`.`{scope.name}`.`{collection}`"
                rows = get_cluster().query(query)

                for row in rows:
                    doc_id = row["id"]
                    try:
                        cb_collection.remove(doc_id)
                    except Exception:
                        pass  # Handle cases where the document was already removed concurrently
