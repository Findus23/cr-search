#!/bin/bash
rsync -rvzP web/dist/ lukas@lw1.at:/srv/server/crsearch/dist/ --fuzzy --delete-after -v
