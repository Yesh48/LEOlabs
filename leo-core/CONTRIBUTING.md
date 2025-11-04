# Contributing to Leo Core

Thanks for your interest in helping build Leo Core! This project powers the LeoRank visibility scoring engine and depends on a friendly, reliable contributor workflow. Contributions of all kinds are welcome—from documentation fixes to new agents and deployment tooling.

## Getting Started
1. Fork the repository and create a feature branch from `main` (e.g. `feat/langsmith-ingestion`).
2. Install the project along with test tooling:
   ```bash
   pip install -r requirements.txt
   pip install .[test]
   ```
3. Verify your environment by running the test suite:
   ```bash
   pytest -v
   ```

## Development Guidelines
- Follow [PEP 8](https://peps.python.org/pep-0008/) and keep type hints intact. Favor pure functions for agent logic and avoid hidden side effects.
- Commit messages **must** follow the [Conventional Commits](https://www.conventionalcommits.org/) format, e.g. `feat: add sitemap crawler` or `fix: handle empty schema markup`.
- Update or add unit tests for any new behavior. LangGraph agents, utilities, and API surfaces should remain deterministic under test.
- Keep documentation in sync. Update `README.md`, `Agents.md`, or `docs/architecture.md` when changing workflows, metrics, or deployment options.
- Note breaking changes or significant features in `CHANGELOG.md` under the current release heading.

## Pull Request Checklist
Before opening a PR, ensure the following commands succeed locally:

```bash
flake8
pytest -v
python cli.py audit https://example.com --no-persist
helm lint charts/leo-core
```

If you are changing container or deployment logic, also verify the Docker image builds:

```bash
docker build -t leo-core:0.2.0 .
```

Include a summary of changes, testing performed, and any follow-up work in the pull request template. Reference related issues where possible.

## Code Review Expectations
- PRs should remain focused on a single improvement. If your work spans multiple concerns (e.g. new agent plus chart updates), consider splitting into separate PRs.
- Address review feedback promptly and prefer additional commits over force-pushing until the PR is approved.
- Document architectural decisions or noteworthy trade-offs in the PR description and, when applicable, `docs/`.

## Contributor License Agreement
By opening a pull request you confirm that you have the right to license your contribution under the MIT License and agree that your code may be distributed under that license.

## Need Help?
Open a discussion or issue if you get stuck. We love hearing about new metric ideas, platform integrations, and automation improvements.

Thank you for helping grow the Leo Core ecosystem!
