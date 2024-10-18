# 3. Code Linting, Formatting, and Type Checking

Date: 2024-10-17

## Status

Accepted on 2024-10-17

Amended by [0007-don-t-use-type-checking-for-tests.md](0007-don-t-use-type-checking-for-tests.md) on 2024-10-17 

## Context

We want to have a consistent source code style and format across the project. Although we are working with Python, we also want to have type checking in our codebase to enhance code quality and reliability.

## Decision

We have decided to implement the following tools for code linting, formatting, and type checking:

1. **Ruff**: Although isort and black are common in the Python community, we believe using [ruff](https://astral.sh/ruff) to lint and format our codebase is a better choice. It does the same thing as isort and acts as an in-place replacement for black while being faster.

2. **Mypy**: For static typing, we will adopt the widely accepted standard [mypy](https://www.mypy-lang.org/). Mypy provides static typing to Python and catches type-related errors at build time, enhancing code reliability and maintainability.


## Consequences

1. **Consistent Code Style**: Using ruff will ensure a consistent code style across the project, improving readability and maintainability.

2. **Faster Linting and Formatting**: Ruff's performance advantages will lead to quicker code checks and formatting, potentially improving developer productivity.

3. **Enhanced Code Quality**: Mypy's static type checking will help catch type-related errors early in the development process, leading to more robust code.

4. **Learning Curve**: We will need to agree on rules from ruff to use and which ones to ignore. This may require some initial setup and team discussion.

5. **Strict Typing Requirements**: We need to ensure our code is correctly typed from the beginning to comply with mypy. This may require additional effort during the initial implementation but will pay off in terms of code quality and maintainability.

6. **Potential Performance Concerns**: As noted, mypy can be slow. We need to investigate caching or other speed-up methods to mitigate this issue.
