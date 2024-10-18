# 1. Use Python as programming language

Date: 2024-10-17

## Status

Accepted on 2024-10-17

Used by [0002-use-pyproject.toml-for-project-setup.md](0002-use-pyproject.toml-for-project-setup.md) on 2024-10-17

## Context

As we begin our project, we need to choose a primary programming language that aligns with our current needs and constraints. We are in an experimental phase where rapid development and iteration are crucial.

## Decision

We have decided to use Python as our primary programming language for this project.

The reasons for this decision are:

1. Wide adoption: Python is one of the most widely used programming languages.

2. Rapid development: Python's syntax and extensive library ecosystem allow for quick prototyping and implementation, which is crucial in our current experimental phase.

3. Versatility: Python can be used for a wide range of applications, from web development to data analysis and machine learning, giving us flexibility as our project evolves.

4. Low barrier to entry: Python's readability and relatively gentle learning curve make it easier for new team members to onboard and contribute quickly.

## Consequences

Positive consequences:
- Faster development cycles and easier prototyping
- Access to a vast ecosystem of libraries and frameworks
- Easier recruitment of developers familiar with the language
- Flexibility to pivot or expand the project's scope if needed

Potential challenges and risks:
- Application runtime speed may become a concern as the project scales, though this is not a current priority
- Distribution of the final application is more complex compared to compiled languages

Future considerations:
- We may need to create specific tools using languages like Rust or Go for easier distribution or improved performance in certain areas
- There's a possibility that we might need to rewrite parts of or the entire application in a different language if performance or distribution becomes a critical factor

