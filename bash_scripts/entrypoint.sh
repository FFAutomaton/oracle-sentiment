#!/bin/bash

echo "Docker container has been started ..."
echo "Starting ..." >> /app/logs/oracle-sentiment.log 2>&1
python --version

# Setup a cron schedule
crontab ./bash_scripts/schedule.txt
cron -f
