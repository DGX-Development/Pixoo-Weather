# Attribution and Provenance

This project is a customized Pixoo-64 weather dashboard derived from an earlier
Python weather display project.

## Known Sources

- Original weather dashboard: https://github.com/jankornfeld/pixoo-weather
- `pixoo-rest` bridge referenced by the original project README:
  https://github.com/ankit-kapur/pixoo-rest
- Current/maintained `pixoo-rest` repository visible on GitHub:
  https://github.com/4ch1m/pixoo-rest
- Weather data service: Open-Meteo forecast API, https://open-meteo.com/
- Moon/weather icon silhouette references:
  - Google Maps Platform weather condition icons documentation:
    https://developers.google.com/maps/documentation/weather/weather-condition-icons
  - Google weather clear icon SVG:
    https://maps.gstatic.com/weather/v1/clear.svg
  - Erik Flowers Weather Icons:
    https://github.com/erikflowers/weather-icons

## Upstream Weather Dashboard

Original project:

```text
Project: pixoo-weather
Author/account: jankornfeld
Repository: https://github.com/jankornfeld/pixoo-weather
Description: A python script that creates an image with weather information for the pixoo 64
Default branch at verification time: master
Observed repository state: public GitHub repository with 8 commits
License: no license file was visible in the repository file list at verification time
Verified: 2026-06-05
```

Original README text preserved from upstream:

```text
pixoo-weather

A python script that gets the weather information from an api and displays it on the pixoo 64. The script will call the rest api from the pixoo-rest project to send the created gif.

The script will generate a new gif every minute (to keep the time almost up-to-"time") and will fetch the newest weather data every five minutes.

Currently you need to start pixoo-rest by yourself.

How it looks like atm

drwaing

How to start

    Pull repo
    Install dependencies

pip install -r requirements.txt

    Update .env with your data
    run python script

python app.py

My Ideas

    Add more faces/icons for current weather
    Add current temp from sensor outside
    Update weather codes from api (cause I still don't know whats correct)
    Start pixoo-rest server automatically
    Do something against the blinking when gif is being uploaded (get rid of loading screen)
```

Important licensing note:

The upstream weather dashboard did not visibly include a `LICENSE` file when
checked. Absence of a license does not mean public-domain or unrestricted use.
Before making this derivative repository public or redistributing it as open
source, confirm permission/license status from the upstream author or repository
history, or replace inherited code with new implementation work. A public GitHub
repository can be source-visible without granting reuse rights, but the README
and repo settings should not imply an open-source license until this is resolved.

## Pixoo REST Bridge

The original weather project's README says it calls the REST API from the
`pixoo-rest` project to send the generated GIF.

The current app posts to `http://localhost:5000/image` in its default static-image
mode. Optional GIF mode posts to `http://localhost:5000/sendGif`.
See [Refresh flicker notes](docs/workflow.md#refresh-flicker-notes) for upload settings.

`pixoo-rest` attribution:

```text
Project: Pixoo REST
Repository: https://github.com/4ch1m/pixoo-rest
License: MIT license
Description: A RESTful API to easily interact with Wi-Fi enabled Divoom Pixoo devices
```

## Local Custom Work

Custom changes in this repository include renderer refactoring, Pixoo-64 layout
work, static-image upload support, systemd/service tooling, local preview/editor
tooling, Open-Meteo WMO weather-code mapping, and function-drawn pixel weather
icons.

The current icon artwork is custom function-drawn pixel art for the Pixoo-64.
External weather icon projects and app icons were used only as visual references
during discussion; the active icons are not direct SVG or PNG copies.
