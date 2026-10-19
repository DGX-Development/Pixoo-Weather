#!/bin/bash
set -euo pipefail

PROJECT_DIR="${PIXOO_WEATHER_DIR:-/home/pi/pixoo-weather}"
SYSTEMD_DIR="/etc/systemd/system"

echo "Installing Pixoo systemd services..."

sudo cp "$PROJECT_DIR/systemd/pixoo-rest.service" "$SYSTEMD_DIR/pixoo-rest.service"
sudo cp "$PROJECT_DIR/systemd/pixoo-weather.service" "$SYSTEMD_DIR/pixoo-weather.service"

sudo systemctl daemon-reload
sudo systemctl enable pixoo-rest.service
sudo systemctl enable pixoo-weather.service

sudo systemctl restart pixoo-rest.service
sudo systemctl restart pixoo-weather.service

echo "Installed and started services."
echo
echo "Check status:"
echo "  sudo systemctl status pixoo-rest.service"
echo "  sudo systemctl status pixoo-weather.service"
echo
echo "Follow logs:"
echo "  journalctl -u pixoo-rest.service -f"
echo "  journalctl -u pixoo-weather.service -f"
