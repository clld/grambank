#!/bin/bash
psql -d glottolog3 -A --field-separator='+++' -t -f query_languages.sql -o languages.csv
psql -d glottolog3 -A --field-separator='+++' -t -f query_macroareas.sql -o macroareas.csv
python coverage.py
cp *.json ../static
