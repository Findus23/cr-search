#!/bin/bash
rsync -rvzP dist/ lukas@lw1.at:/srv/server/crsearch/dist/ --fuzzy --delete-after -v
