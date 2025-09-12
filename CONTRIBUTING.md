# Contributing

First off, thank you for considering contributing! All PRs are welcome and help is much appreciated.

## Getting Started

1.  Fork the repository on GitHub.
2.  Clone your forked repository locally:
    ```sh
    git clone https://github.com/dunderrrrrr/blocket_api.git
    cd blocket_api
    direnv allow
    ```
3.  Create a new branch for your changes:
    ```sh
    git checkout -b my-awesome-feature
    ```

## Development Setup

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency management and as a runner.

1.  Install `uv`:
    ```sh
    pip install uv
    ```
2.  Create a virtual environment and install dependencies:
    ```sh
    uv venv
    uv sync
    ```
3.  Set up the pre-commit hooks:
    ```sh
    pre-commit install
    ```

### Nix Development

If you have `nix` with `flakes` enabled, you can use the provided `flake.nix` to enter a development shell.

```sh
nix develop
```

This will provide you with a shell with `python`, `uv`, and `ruff` installed. It will also set up a virtual environment, install all dependencies (including `pytest`), and configure the pre-commit hooks for you. You can then run the tests as described in the "Running Tests" section.

## Running Tests

To run the test suite, use the following command:

```sh
uv run pytest
```

Before submitting your changes, please also run the following checks:

```sh
uv run ruff check .
uv run mypy .
```

## Submitting Pull Requests

1.  Commit your changes with a clear and descriptive commit message. Please try to follow the [Conventional Commits](https://www.conventionalcommits.org/) specification if possible.
2.  Push your changes to your forked repository:
    ```sh
    git push origin my-awesome-feature
    ```
3.  Open a pull request on the original repository. When you open a pull request, the test suite will be run automatically by our GitHub workflow.
4.  Please make sure your PR is up to date with the `main` branch of the original repository. You can do this by running `git pull upstream main` in your branch.
