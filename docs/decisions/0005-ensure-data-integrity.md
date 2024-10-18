# 5. Ensure data integrity

Date: 2024-10-17

## Status

Accepted on 2024-10-17

Builds on [0004-event-driven.md](0004-event-driven.md) on 2024-10-17

## Context

We want to ensure the integrity of the data throughout its lifecycle. We need a robust mechanism to verify that the data has not been tampered with during transmission or storage over time.

## Decision

We have decided to use RSA digital signatures to ensure data integrity across our system.

## Consequences

1. Enhanced security: RSA signing provides a cryptographically secure method to detect any unauthorized modifications to the data.
2. Non-repudiation: The use of digital signatures also provides proof of data origin, as only the holder of the private key can create valid signatures. If we would expose the data to a third party, we can use the signature to prove that we are the source of the data.
3. Compatibility: RSA is a widely supported algorithm, ensuring compatibility with various systems and libraries.

### Challenges and risks:

Using RSA signing introduces performance overhead, implementation and key management complexity. 
