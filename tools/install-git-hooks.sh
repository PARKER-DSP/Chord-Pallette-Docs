#!/usr/bin/env sh
set -e

REPO_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$REPO_ROOT"

git config core.hooksPath .githooks
echo "Git hooks path configured: .githooks"
echo "Pre-commit hook will run docs nav sync and validation checks."
