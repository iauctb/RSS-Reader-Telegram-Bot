#!/bin/bash

set -e

cd "$(dirname "$0")"

python ./bot/bot.py
python ./bot/cron.py

