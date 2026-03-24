#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

IMAGE="cheatsheets-builder"
docker build -q -t "$IMAGE" .

if [ $# -eq 0 ]; then
  scripts=$(ls src/*_cheatsheet.py)
else
  scripts=""
  for name in "$@"; do
    scripts="$scripts src/${name}_cheatsheet.py"
  done
fi

for s in $scripts; do
  echo "Building $s ..."
  docker run --rm -v "$PWD:/app" "$IMAGE" python "$s"
done

echo "Generated:"
ls -lh *.pdf
