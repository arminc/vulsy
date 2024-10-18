# 2. Use pyproject.toml for project setup

Date: 2024-10-17

## Status
 
Accepted on 2024-10-17

Builds on [0001-use-python-as-programming-language.md](0001-use-python-as-programming-language.md) on 2024-10-17

## Context

There's ongoing debate in the Python community about the use of pyproject.toml, individual configuration files, and requirements.txt. This ADR aims to clarify our stance on this matter.

## Decision

We endorse the use of pyproject.toml for comprehensive project configuration. While still a topic of discussion in the Python community, we believe that using one file simplifies the configuration process, promoting consistency and reducing complexity.

## Consequences

- Improved consistency: Having all configuration in one place promotes a more consistent approach across the project.
- Tool compatibility: Some older tools or systems might not fully support pyproject.toml, which could require additional steps or workarounds.
- Requirements.txt generation: For scanning purposes or backward compatibility, we may need to generate a full requirements.txt file from the pyproject.toml configuration.
