#!/usr/bin/env sh
# Serve the static site locally from static-html/ (no build step).
set -e
cd "$(dirname "$0")/../static-html"
python3 -m http.server 4173
