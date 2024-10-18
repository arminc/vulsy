# Run

We are using a Makefile to run things, just run `make` to see all options.

To be able to run the application you need some environment variables set. For all the options and description what they do see [settings.py](/reference/vulsy/settings). By default the application will run without tracing, to enable tracing run make with `run-with-otel` instead of `run`.

The bare minimum you need to set is:

```bash
COUCHBASE_INIT_URL="http://localhost"
COUCHBASE_URL="couchbase://localhost"
COUCHBASE_USERNAME="admin"
COUCHBASE_PASSWORD="password"
SOURCE_NVD_API_KEY="KEY"
RSA_PRIVATE_KEY_PASSWORD="vulsy"
LOGGING_LEVEL=INFO
TELEMETRY_DEV=true
``` 

Optional settings to enable OpenTelemetry:

```bash
OTEL_SERVICE_NAME="vulsy"
OTEL_TRACES_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true


## Run tests

To run unit tests you can run `make test`.

To run the all the tests you need to have a running Couchbase server. You can start one with `make docker up test-db`. Then run `make run couchbase full` to configure the test database. After that you can run `make test-all` to run all the tests.