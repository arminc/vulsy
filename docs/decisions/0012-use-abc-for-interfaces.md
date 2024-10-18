# 12. Use ABC for interfaces

Date: 2024-10-17

## Status

Accepted on 2024-10-17  


## Context

We need a way to define interfaces for our repositories.

## Decision

Although Python's typing system is newer and offers more flexibility, using Abstract Base Classes (ABC) for interfaces enhances code navigation in IDEs. This approach allows developers to easily find implementations and understand the structure of the codebase.

## Consequences

This decision simplifies the process of locating class implementations and promotes better code organization, though it may introduce some overhead in defining ABCs.
