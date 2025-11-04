# Contributing to Leo Core

Thanks for your interest in helping build Leo Core! This project aims to provide a transparent, extensible visibility scoring pipeline powered by LangGraph agents. Contributions of all kinds are welcome.

## Getting Started
1. Fork the repository and create a feature branch from `main`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install .[test]
   ```
3. Run the automated test suite to verify your environment:
   ```bash
   pytest
   ```

## Development Guidelines
- Follow existing code style and type hints. Pydantic models and agent functions should remain deterministic and side-effect free.
- Include unit tests for new functionality, especially for agent behaviors and utilities.
- Document configuration or metric changes in `specs/leo-specs.yml` and update the README when introducing new features.
- Keep commits focused and reference relevant issues in your pull request description.

## Pull Requests
- Ensure `pytest` passes locally before opening a PR.
- Provide a clear summary of changes, testing performed, and any deployment considerations.
- New agents or metrics should include sample output updates in `examples/` when applicable.

## Community Support
Questions or ideas? Open a GitHub issue to start a discussion. We welcome proposals for new metrics, integration adapters, or tooling improvements.

Thank you for helping grow the Leo Core ecosystem!
