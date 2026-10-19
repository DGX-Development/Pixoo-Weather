#!/bin/bash
set -e

echo "Starting pixoo-rest..."
cd "${PIXOO_REST_DIR:-/home/pi/pixoo-rest}"
source .venv/bin/activate
python -m pixoo_rest.main &
REST_PID=$!

sleep 3

echo "Starting pixoo-weather..."
cd "${PIXOO_WEATHER_DIR:-/home/pi/pixoo-weather}"
source .venv/bin/activate
python app.py &
WEATHER_PID=$!

echo "pixoo-rest PID: $REST_PID"
echo "pixoo-weather PID: $WEATHER_PID"
echo "Press CTRL+C to stop both."

trap "echo 'Stopping...'; kill $REST_PID $WEATHER_PID; exit" INT TERM

wait
