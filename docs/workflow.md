# Setup and Runtime Guide

[Back to the project README](../README.md) · [Dashboard editor](dashboard-editor.md)

Install, configure, run, and update the dashboard with this guide.

## Project Overview

This project uses:

- Windows, macOS, or Linux computer
- Python
- Raspberry Pi 3 Model B or similar Pi
- Divoom Pixoo-64
- `pixoo-rest` local bridge
- `pixoo-weather` dashboard renderer

The Raspberry Pi runs the dashboard. A desktop or laptop can generate previews.

## Initial setup

On the Raspberry Pi, install the separate [pixoo-rest bridge](https://github.com/4ch1m/pixoo-rest)
using its own installation instructions. Its Python environment and this
dashboard's environment are separate. The runtime examples below assume the
bridge is installed at `~/pixoo-rest` with a `.venv` environment.

From this dashboard's project folder on the Pi, create and activate its environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

If Python reports that `venv` is unavailable, install the virtual-environment
support for your Pi's Python version first. These commands use a Linux shell.
For local Windows preview work, create the environment with `py -m venv .venv`
and activate it with `.\.venv\Scripts\Activate.ps1` in PowerShell before installing
the same requirements.

Next, complete [Required configuration](#required-configuration), then follow
[Manual runtime](#manual-runtime) to start the bridge and dashboard in separate
terminals. Folder names and usernames in the examples are defaults; adjust them
for your installation.

## Required Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Update `.env` for your setup:

```text
HOST="<PIXOO_IP_OR_HOSTNAME>"
LATITUDE="<YOUR_LATITUDE>"
LONGITUDE="<YOUR_LONGITUDE>"
TIMEZONE="auto"
```

Use an IANA timezone such as `America/New_York` if you do not want Open-Meteo
to infer timezone automatically.

Do not commit `.env`. It contains local device/location configuration.

## Common Paths

Typical Pi folders:

```text
/home/pi/pixoo-weather
/home/pi/pixoo-rest
```

If your Pi user or folders differ, pass script parameters or edit the copied
systemd service files before installing them.

Typical Pi host:

```text
pi@pixoo64.local
```

If `.local` name resolution does not work, use the Pi hostname or IP address:

```text
pi@pixoo64
pi@<PI_IP_ADDRESS>
```

## One-Time SSH Key Setup

From Windows PowerShell:

```powershell
cd <LOCAL_PROJECT_FOLDER>
powershell -ExecutionPolicy Bypass -File .\scripts\setup-ssh-key.ps1 -PiHost pi@pixoo64.local
```

This creates a local SSH key if needed, installs the public key on the Pi, and
verifies key login. After this succeeds, deploy/start scripts should not ask for
the Pi password every time.

If your Pi uses a different username or address:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-ssh-key.ps1 -PiHost <user>@<PI_IP_ADDRESS>
```

## Manual Runtime

Two processes are required.

Start `pixoo-rest` first:

```bash
cd ~/pixoo-rest
source .venv/bin/activate
python -m pixoo_rest.main
```

Leave that terminal open.

Start `pixoo-weather` in a second terminal:

```bash
cd ~/pixoo-weather
source .venv/bin/activate
python app.py
```

Leave that terminal open too.

## Temporary One-Command Start

Before systemd is installed, you can start both processes from the Pi:

```bash
cd ~/pixoo-weather
chmod +x scripts/start-pixoo-weather.sh
./scripts/start-pixoo-weather.sh
```

The script uses these defaults:

```text
PIXOO_REST_DIR=/home/pi/pixoo-rest
PIXOO_WEATHER_DIR=/home/pi/pixoo-weather
```

Override them if your folders differ:

```bash
PIXOO_REST_DIR=/home/<user>/pixoo-rest PIXOO_WEATHER_DIR=/home/<user>/pixoo-weather ./scripts/start-pixoo-weather.sh
```

From Windows PowerShell:

```powershell
cd <LOCAL_PROJECT_FOLDER>
powershell -ExecutionPolicy Bypass -File .\scripts\start-on-pi.ps1 -PiHost pi@pixoo64.local
```

Press `CTRL+C` in that PowerShell window to stop both remote processes.

Do not use `start-on-pi.ps1` as the normal daily command after systemd is
installed. It is a foreground troubleshooting helper.

## Deploy From Windows To Pi

Run after local code changes:

```powershell
cd <LOCAL_PROJECT_FOLDER>
powershell -ExecutionPolicy Bypass -File .\scripts\deploy-to-pi.ps1 -PiHost pi@pixoo64.local
```

The deploy script copies:

- application Python modules
- `icon_sets/`
- `scripts/`
- `systemd/`
- `requirements.txt`
- `3x5pixel.ttf`

It does not copy `.env` by default. Copy `.env` intentionally only when local
runtime settings changed:

```powershell
scp .env pi@pixoo64.local:/home/pi/pixoo-weather/.env
```

## Restart After Deploy

If systemd services are installed, restart the weather app after deploy:

```powershell
ssh -t pi@pixoo64.local "sudo systemctl restart pixoo-weather.service"
```

Restart both services:

```powershell
ssh -t pi@pixoo64.local "sudo systemctl restart pixoo-rest.service pixoo-weather.service"
```

Check status:

```powershell
ssh pi@pixoo64.local "systemctl status pixoo-rest.service pixoo-weather.service --no-pager -l"
```

Follow logs:

```powershell
ssh pi@pixoo64.local "journalctl -u pixoo-weather.service -f"
```

Remote `sudo` commands use `ssh -t` so the Pi can prompt for the sudo password.
Plain status checks do not need `sudo`.

## Installing systemd Services

Deploy the latest files first:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\deploy-to-pi.ps1 -PiHost pi@pixoo64.local
```

SSH to the Pi:

```powershell
ssh pi@pixoo64.local
```

Install services on the Pi:

```bash
cd ~/pixoo-weather
chmod +x scripts/install-systemd-services.sh
./scripts/install-systemd-services.sh
```

This installs and starts:

- `pixoo-rest.service`
- `pixoo-weather.service`

The included service files assume:

```text
User=pi
/home/pi/pixoo-rest
/home/pi/pixoo-weather
```

If your Pi uses different paths, edit `systemd/*.service` on the Pi before
running the installer.

After systemd is installed, normal Pi reboot should start both services
automatically.

## Local Testing

Syntax check:

```bash
python -m py_compile app.py renderer.py functions.py weatherresponse.py colors.py make_weather_code_legend.py make_dashboard_mockup.py make_icon_baseline_previews.py
```

Generate the weather-code preview page:

```bash
python make_weather_code_legend.py
```

Open:

```text
preview.html
```

For the editable dashboard/icon grid, follow [Generate the editor](dashboard-editor.md#generate-the-editor).

Generate icon baseline sheets:

```bash
python make_icon_baseline_previews.py
```

Outputs:

```text
mockups/function-current-icon-baseline.png
mockups/function-forecast-icon-baseline.png
```

More editor details are in [dashboard-editor.md](dashboard-editor.md).

## Temporary Icon Override

For physical Pixoo icon/layout testing, the renderer can temporarily fake the
displayed weather icons without changing fetched weather data.

Example `.env` values:

```text
PIXOO_TEST_CURRENT_WEATHER_CODE="95"
PIXOO_TEST_CURRENT_IS_DAY="1"
PIXOO_TEST_FORECAST_WEATHER_CODES="0,3,61,95"
```

To disable overrides:

```text
PIXOO_TEST_CURRENT_WEATHER_CODE=""
PIXOO_TEST_CURRENT_IS_DAY=""
PIXOO_TEST_FORECAST_WEATHER_CODES=""
```

The override affects icons only. Temperatures, dates, and day labels still come
from the normal weather payload and clock.

## Icon Revert Process

The preserved original-style icon renderer is available as:

```text
legacy_pixel
```

Use it in `.env`:

```text
PIXOO_ICON_SET="legacy_pixel"
```

Use the active icon set:

```text
PIXOO_ICON_SET="premium_pixel"
```

The legacy icon set remains available as a fallback.

## Time And Weather Architecture

Clock/date/day come from the Raspberry Pi system clock.

The Pi should sync time from normal Linux network time sync.

Weather comes from Open-Meteo.

Current conditions request:

```text
temperature_2m, weather_code, is_day
```

The renderer uses `is_day` only for the current-condition icon. Daily forecast
icons remain based on the daily WMO weather-code summary.

Desired weather failure behavior:

```text
If weather fetch succeeds:
    update cached weather data

If weather fetch fails:
    keep rendering clock/date/day using Pi system time
    keep using last known weather data
    do not crash
    do not blank the display
```

Full last-known-good weather caching is not implemented.

## Refresh Flicker Notes

The Pixoo may show an hourglass/loading interstitial when a new animation or GIF
payload is uploaded.

The dashboard defaults to static PNG upload through `pixoo-rest`'s `/image`
endpoint:

```text
PIXOO_UPLOAD_MODE="image"
```

Current refresh controls:

```text
DISPLAY_REFRESH_INTERVAL_SECONDS="60"
PIXOO_UPLOAD_MODE="image"
GIF_FRAME_DURATION_MS="60000"
ENABLE_BLINK_ANIMATION="False"
```

At the default 60-second interval, dashboard refreshes align to the Raspberry
Pi's real minute boundary. The app hashes rendered bytes and skips Pixoo upload
if the output did not change.

Blinking colon animation requires changing pixels between minute updates and
can bring back frequent visible refresh behavior. Keep it off unless transport
testing proves an animation path that does not show the hourglass.

## Weather Icon Fallback Philosophy

Every supported Open-Meteo WMO weather code should intentionally map to a visual
icon. There should be no blank states and no crashes.

Unexpected or unmapped weather codes render a distinct gray unknown-weather icon:

```python
icon_key = WEATHER_ICON_MAP.get(code, "weather_unknown")
```

Visual distinction matters:

- mostly sunny is not partly cloudy
- drizzle is not freezing drizzle
- rain is not freezing rain
- showers are not steady rain
- thunderstorm is not hailstorm
