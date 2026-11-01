#!/usr/bin/env bash
# Semantic-release has already stamped pyproject.toml before invoking this hook.
set -euo pipefail

# The PSR Docker action has Python/pip but does not provide uv. Local developers
# normally already have uv; bootstrap it only inside the Docker action if missing.
if ! command -v uv >/dev/null 2>&1; then
    if [ "${PSR_DOCKER_GITHUB_ACTION:-}" != "true" ]; then
        echo "Install uv before running the release build." >&2
        exit 1
    fi
    python -m pip install uv
fi

uv lock --upgrade-package hilbertplot
uv lock --check
uv build
