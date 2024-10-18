# 4. Event driven

Date: 2024-10-17

## Status

Accepted on 2024-10-17

Used by [0009-vulnerability-data-ingestion-process.md](0009-vulnerability-data-ingestion-process.md) on 2024-10-17

Used by [0005-ensure-data-integrity.md](0005-ensure-data-integrity.md) on 2024-10-17

## Context

We need a way to maintain a clear record of what has happened within the system. This is crucial for auditing, debugging, and understanding the state of the application at any given time. Additionally, we want the ability to replay steps when we get new ideas or need to test different scenarios.

## Decision

We have decided to implement an event-driven architecture where appropriate within our application. This means:

1. Key actions and state changes will be recorded as events.
2. These events will be stored in a persistent store.
3. Parts of the system can react to these events as needed.
4. The system will support replaying events to test new ideas or scenarios.

## Consequences

### Positive

- Improved traceability of system actions and state changes.
- Easier to implement audit trails and historical views of data.
- Increased flexibility in adding new features that depend on past events.
- Ability to replay events for testing new ideas and scenarios.

### Negative

- Increased complexity in system design and implementation.
- Potential performance overhead due to event storage and processing.
- Potential storage overhead due to storing data multiple times.
- Additional complexity in managing event replay functionality.
