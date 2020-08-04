#!/bin/bash
cp db_dev.sqlite3 db_prod.sqlite3
git add .
git commit -m $1
git push