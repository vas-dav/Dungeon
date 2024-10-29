#! /bin/sh

export DB_PASSWORD="UJ4tDsE39bT!"
export DB_SERVER="192.168.100.95"

python3 -m flask --app /app/src/server.py run --host=0.0.0.0
