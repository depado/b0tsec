#!/bin/bash
until server_bot.py; do
    echo "Bot crashed with exit code $?. Restarting..." >&2
    sleep 1
done