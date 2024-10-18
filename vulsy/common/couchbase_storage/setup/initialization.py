"""Couchbase server initialization."""

import logging
import sys
import time

from vulsy.common.http import client
from vulsy.settings import settings

logger = logging.getLogger(__name__)
HTTP_200 = 200


def _check_couchbase_status(url: str) -> None:
    """Check if the Couchbase server is ready.

    Args:
        url: The URL to check the Couchbase server status.
    """
    for _ in range(20):
        try:
            response = client.http_request(url)
            if response.status_code == HTTP_200:
                return
            logger.info("Couchbase server is not ready yet.")
        except Exception:  # noqa: BLE001
            logger.info("Couchbase server is not ready yet.")
        time.sleep(1)


def initialize_couchbase_server() -> None:
    """Initialize new Couchbase server.

    This function initializes a new Couchbase server by for example setting the username and password.
    This does not create buckets or collections.
    """
    url = f"{settings.couchbase.init_url}:{settings.couchbase.port}/settings/web"
    data = {
        "port": settings.couchbase.port,
        "username": settings.couchbase.username,
        "password": settings.couchbase.password.get_secret_value(),
    }

    # Set up Couchbase services
    services_url = f"{settings.couchbase.init_url}:{settings.couchbase.port}/node/controller/setupServices"
    _check_couchbase_status(services_url)
    services_data = {"services": "kv,n1ql,index,fts"}
    services_response = client.http_request(services_url, client.HTTPMethod.POST, data=services_data)
    if services_response.status_code == HTTP_200:
        logger.info("Couchbase services set up successfully.")
    else:
        logger.error("Failed to set up Couchbase services: %s", services_response.text)
        sys.exit(1)

    # Set up Couchbase admin credentials
    response = client.http_request(url, client.HTTPMethod.POST, data=data)
    if response.status_code == HTTP_200:
        logger.info("Couchbase admin credentials set up successfully.")
    else:
        logger.error("Failed to set Couchbase admin credentials: %s", response.text)
        sys.exit(1)
