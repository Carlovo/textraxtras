# Welcome to textraxtras

Extras for Amazon's Textract API.

## Development

Local development cycle to work on this project:

- Create fix, feature etc.
- Format: `uvx ruff format` (and sort imports: `uvx ruff check --select I --fix`)
- Lint: `uvx ruff check`
- Type checking: `uv run mypy .`
- Test: `uv run python -m unittest`
