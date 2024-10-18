# 7. Don't use type checking for tests

Date: 2024-10-17

## Status 

Accepted on 2024-10-17

Amends [0003-code-linting-formatting-and-type-checking.md](0003-code-linting-formatting-and-type-checking.md) on 2024-10-17

## Context

While type checking with mypy is valuable for our main codebase, applying it to our test suite doesn't provide significant benefits. The primary reasons for this decision are:

1. Tests are typically run frequently and errors are caught quickly during execution.
2. Test code is often more flexible and may require more dynamic typing.
3. The overhead of maintaining strict typing in tests can slow down test development and maintenance.

## Decision

We have decided not to use type checking with mypy for our test code.
