#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

IMAGE="cheatsheets-builder"

docker build -t "$IMAGE" .
docker run --rm -v "$PWD:/app" "$IMAGE"

echo "Generated:"
ls -lh *.pdf
