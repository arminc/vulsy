"""Vulsy settings."""

from pathlib import Path
from typing import Self

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from vulsy.common.types.url import HttpUrl


class CouchbaseSettings(BaseSettings):
    """Couchbase-specific settings.

    Attributes:
        init_url (str): The initial URL for connecting to Couchbase used for initializing the database.
        url (HttpUrl): The URL for the Couchbase server.
        username (str): The username for authenticating with Couchbase.
        password (SecretStr): The password for authenticating with Couchbase.
        port (int): The port number for connecting to Couchbase (default is 8091).
    """

    init_url: str
    url: HttpUrl
    username: str
    password: SecretStr
    port: int = 8091

    model_config = SettingsConfigDict(env_prefix="couchbase_")


class SourceSettings(BaseSettings):
    """Source-specific settings.

    Attributes:
        nvd_api_key (str): The API key for the NVD source.
    """

    nvd_api_key: str

    model_config = SettingsConfigDict(env_prefix="source_")


class TelemetrySettings(BaseSettings):
    """Telemetry-specific settings.

    Attributes:
        dev (bool): Whether to run in development mode, configure logging to use console, defaults to `False`.
        service_name (str): The name of the service, defaults to `vulsy`.
        service_instance_id (str): The instance ID of the service, defaults to `dev`.
        logging_level (str): The logging level to use, defaults to `INFO`.
    """

    dev: bool = False
    service_name: str = "vulsy"
    service_instance_id: str = "dev"

    logging_level: str = "INFO"

    @field_validator("logging_level")
    def validate_logging_level(cls: type[Self], value: str) -> str:  # type: ignore [misc]
        """Validate the logging level."""
        allowed_levels = {"DEBUG", "INFO", "WARN", "ERROR"}
        if value not in allowed_levels:
            raise ValueError("logging_level must be one of %s", allowed_levels)
        return value

    model_config = SettingsConfigDict(env_prefix="telemetry_")


class Settings(BaseSettings):
    """Generic settings class that can be extended over time.

    Attributes:
        version (str): The version of the application, defaults to `dev`.
        rsa_private_key_path (Path): The path to the private RSA key, defaults to `tests/data/test-private-key.pem`.
        rsa_private_key_password (SecretStr): The password for the private RSA key.
        rsa_public_key_path (Path): The path to the public RSA key, defaults to `tests/data/test-public-key.pem`.
        logging_level (str): The logging level to use, defaults to `INFO`.


        couchbase (CouchbaseSettings): The Couchbase settings.
        sources (SourceSettings): The source settings.
        telemetry (TelemetrySettings): The telemetry settings.
    """

    version: str = "dev"
    rsa_private_key_path: Path = Path("tests/data/test-private-key.pem")
    rsa_private_key_password: SecretStr
    rsa_public_key_path: Path = Path("tests/data/test-public-key.pem")

    logging_level: str = "INFO"

    couchbase: CouchbaseSettings = CouchbaseSettings()  # type: ignore [call-arg]
    sources: SourceSettings = SourceSettings()  # type: ignore [call-arg]
    telemetry: TelemetrySettings = TelemetrySettings()  # type: ignore [call-arg]


settings = Settings()  # type: ignore [call-arg]
