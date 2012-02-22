#!/bin/bash
ROOT="$HOME/Website"
rm -rf "$ROOT/publish"
mkdir -p "$ROOT/publish"
./scripts/python/generate.py $ROOT/templates/site.html $ROOT/content $ROOT/publish
cd $ROOT/publish
ln -s overview.html index.html
