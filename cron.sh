#!/bin/bash
DIR=`dirname "$0"`
cd $DIR
python3 cron.py
git add _includes/data.html
git commit -m "Updating data"
git push