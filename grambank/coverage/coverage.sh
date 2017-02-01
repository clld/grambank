#!/bin/bash
# expect 10 minutes of runtime
psql -d glottolog-2.7 -A --field-separator='+++' -t -f query_languages.sql -o languages.csv
echo 'ok'
psql -d glottolog-2.7 -A --field-separator='+++' -t -f query_macroareas.sql -o macroareas.csv
echo 'ok'
python coverage.py
cp *.json ../static
