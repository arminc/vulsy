"""Vulsy application."""

import logging
from datetime import datetime

from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry._logs._internal import LogRecord
from opentelemetry.metrics import Meter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.trace import Tracer

from vulsy.settings import settings


def _init_logging() -> None:
    """When developing locally without OpenTelemetry we want to log to the console in a human readable format."""

    # Convert to human readable format when running in dev mode
    def dev_log_message_formatter(record: LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.timestamp / 1e9)  # type: ignore [operator]  # noqa: DTZ006
        return f"{timestamp}|{record.severity_text}| {record.body}\n"

    if settings.telemetry.dev:
        logger_provider = LoggerProvider()
        # This can only be set once
        set_logger_provider(logger_provider)
        exporter = ConsoleLogExporter(formatter=dev_log_message_formatter)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
        handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(settings.telemetry.logging_level)


_init_logging()

# OpenTelemetry is configured from the environment variables
# It does mean we need the opentelemetry-intrument and opentelemetry-distro package to be installed
tracer: Tracer = trace.get_tracer_provider().get_tracer("vulsy")
meter: Meter = metrics.get_meter("vulsy")
