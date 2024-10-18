# 8. Use Typer as cli library

Date: 2024-10-17

## Status

Accepted on 2024-10-17  

## Context

We need to choose a library for creating a CLI in the project.

## Decision

Among the various tools available, our consideration focuses on options like [Click](https://github.com/pallets/click/) and [Typer](https://github.com/tiangolo/typer/), along with others. While Click is a powerful choice, we find Typer to be a simpler and more elegant solution that best meets our project needs.

We have decided to use Typer as our CLI library for this project.

## Consequences

- Typer provides a more intuitive and Pythonic way of creating CLIs.
- It has built-in support for type hints, which aligns well with our use of mypy for static type checking.
- The library offers automatic help generation and command completion, improving the user experience.
- Since Typer utilizes Click underneath, there might be a discussion about why not to use Click directly. 
