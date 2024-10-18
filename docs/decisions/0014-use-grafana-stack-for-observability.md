# 14. Use Grafana stack for observability

Date: 2024-10-17

## Status

Accepted on 2024-10-17

Used by [0013-use-opentelemetry-for-tracing.md](0013-use-opentelemetry-for-tracing.md) on 2024-10-26

## Context

To effectively monitor and visualize OpenTelemetry data locally, we need a robust observability stack. The Grafana stack provides a comprehensive solution that integrates various observability tools.

## Decision

We have decided to implement the Grafana stack for local OpenTelemetry visibility. This includes:
- **Grafana** as the frontend for visualizing metrics and logs.
- **Loki** for aggregating and querying logs.
- **Tempo** for managing and visualizing traces.
- **Mimir** for handling metrics efficiently.

This combination allows us to have a unified view of our observability data, facilitating better debugging and performance monitoring.


