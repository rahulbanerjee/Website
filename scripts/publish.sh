#!/bin/bash
rm -rf /home/banerjee/web/publish
mkdir -p /home/banerjee/web/publish
./scripts/python/generate.py /home/banerjee/web/templates/site.html /home/banerjee/web/content /home/banerjee/web/publish
cd /home/banerjee/web/publish
ln -s overview.html index.html
