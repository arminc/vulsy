"""Vulsy main."""

import logging

import typer
from opentelemetry import trace

from vulsy import meter, tracer
from vulsy.common.couchbase_storage.main import couchbase_app
from vulsy.common.couchbase_storage.repo.transform import TransformationDataRepositoryImpl
from vulsy.settings import settings
from vulsy.vulnerability_pipeline.ingestion.main import ingestion_app
from vulsy.vulnerability_pipeline.transformation.transform import transform as transform_vulsy

# Disable pretty exceptions from typer, it is not needed and clutters the output
app = typer.Typer(pretty_exceptions_enable=False)


app.add_typer(couchbase_app, name="couchbase", help="Couchbase-related commands")
app.add_typer(ingestion_app, name="ingest", help="Ingestion-related commands")


@app.command()
@tracer.start_as_current_span("version")
def version() -> None:
    """Log the Vulsy version."""
    counter = meter.create_counter(
        name="version_counter",
        description="Just a counter to test metrics",
        unit="1",
    )

    counter.add(6, attributes={"test": "version"})
    trace.get_current_span().add_event("This is a version event")
    logging.getLogger().info("Vulsy version %s", settings.version)


@app.command()
@tracer.start_as_current_span("transform")
def transform() -> None:
    """Transform the source item events."""
    transform_vulsy(TransformationDataRepositoryImpl())


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(settings.logging_level)
    app()
