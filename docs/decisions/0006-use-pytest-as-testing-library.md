# 6. Use pytest as testing library

Date: 2024-10-17

## Status

Accepted on 2024-10-17

## Context

We need to choose a testing framework for our Python project. The two main contenders are pytest and unittest, which is part of the Python standard library.

## Decision

We have decided to use pytest as our testing library instead of unittest.

## Consequences

### Positive:

1. Simpler test writing: pytest allows for more concise and readable test code.
2. Powerful fixture system: Makes it easier to set up and manage test dependencies.
3. Extensive plugin ecosystem: Provides additional functionality and integrations.
4. Better test discovery: Automatically finds tests without requiring specific naming conventions.
5. Parameterized testing: Simplifies testing multiple scenarios with less code.

### Negative:

1. Additional dependency: pytest is not part of the standard library and needs to be installed.
