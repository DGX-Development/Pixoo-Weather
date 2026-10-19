import json
import hashlib
import time
from io import BytesIO
from typing import Optional
from urllib.parse import quote

import requests
from dotenv import dotenv_values
from schedule import every, repeat, run_pending

from renderer import render_dashboard
from weatherresponse import WeatherResponse, weather_response_object_hook


env = dotenv_values(".env")
weatherData: Optional[WeatherResponse] = None
lastSentDigest: Optional[str] = None


def env_bool(name, default=False):
    value = env.get(name)
    if value is None:
        return default
    return str(value).strip().lower() in ("1", "true", "yes", "on")


DISPLAY_REFRESH_INTERVAL_SECONDS = int(env.get("DISPLAY_REFRESH_INTERVAL_SECONDS", 60))
GIF_FRAME_DURATION_MS = int(env.get("GIF_FRAME_DURATION_MS", 60000))
ENABLE_BLINK_ANIMATION = env_bool("ENABLE_BLINK_ANIMATION", False)
PIXOO_UPLOAD_MODE = env.get("PIXOO_UPLOAD_MODE", "image").strip().lower()
WEATHER_TIMEZONE = env.get("TIMEZONE", "auto")


def weather_url():
    return (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={env['LATITUDE']}"
        f"&longitude={env['LONGITUDE']}"
        "&current=temperature_2m,weather_code,is_day"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min"
        f"&timezone={quote(WEATHER_TIMEZONE, safe='')}"
        "&temperature_unit=fahrenheit"
    )


def drawImage(blink):
    if weatherData is None:
        raise RuntimeError("Weather data has not been fetched yet.")

    image = render_dashboard(weatherData, blink=bool(blink))

    if env.get("PREVIEW") == "True":
        image.show()

    return image


def render_gif_bytes():
    if ENABLE_BLINK_ANIMATION:
        images = [drawImage(0), drawImage(1)]
        buffer = BytesIO()
        images[0].save(
            buffer,
            format="GIF",
            save_all=True,
            append_images=images[1:],
            duration=1000,
            loop=0,
        )
        return buffer.getvalue()

    # Single-frame GIFs let pixoo-rest use draw_image/push instead of the
    # animated GIF reset/send path that can trigger the Pixoo hourglass.
    image = drawImage(0)
    buffer = BytesIO()
    image.save(
        buffer,
        format="GIF",
        duration=GIF_FRAME_DURATION_MS,
        loop=0,
    )
    return buffer.getvalue()


def render_image_bytes():
    image = drawImage(0)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def render_upload_payload():
    if ENABLE_BLINK_ANIMATION or PIXOO_UPLOAD_MODE == "gif":
        return "gif", "image.gif", "image/gif", render_gif_bytes()

    return "image", "image.png", "image/png", render_image_bytes()


def run():
    global lastSentDigest

    if weatherData is None:
        return

    upload_mode, filename, content_type, payload = render_upload_payload()
    digest = hashlib.sha256(payload).hexdigest()

    if digest == lastSentDigest:
        prints("dashboard unchanged; skipping Pixoo upload")
        return

    with open(filename, "wb") as image_file:
        image_file.write(payload)

    if upload_mode == "gif":
        response = requests.post(
            "http://localhost:5000/sendGif",
            files={"gif": (filename, BytesIO(payload), content_type)},
            data={"speed": "1000"},
            timeout=15,
        )
    else:
        response = requests.post(
            "http://localhost:5000/image",
            files={"image": (filename, BytesIO(payload), content_type)},
            data={"x": "0", "y": "0", "push_immediately": "true"},
            timeout=15,
        )

    response.raise_for_status()
    lastSentDigest = digest


def next_display_refresh_at(timestamp=None):
    timestamp = time.time() if timestamp is None else timestamp

    if DISPLAY_REFRESH_INTERVAL_SECONDS == 60:
        return timestamp - (timestamp % 60) + 60

    return timestamp + DISPLAY_REFRESH_INTERVAL_SECONDS


@repeat(every(int(env.get("FETCH_INTERVAL", 5))).minutes)
def fetchWeatherData():
    global weatherData

    prints("fetching newest weather data")

    response = requests.get(weather_url(), timeout=15)
    response.raise_for_status()

    weatherData = json.loads(
        response.text,
        object_hook=weather_response_object_hook,
    )


def prints(value):
    if env.get("DEBUG") == "True":
        print(value)


def main():
    fetchWeatherData()
    run()
    next_display_refresh = next_display_refresh_at()

    while True:
        run_pending()

        if time.time() >= next_display_refresh:
            run()
            next_display_refresh = next_display_refresh_at()

        sleep_for = min(1, max(0.1, next_display_refresh - time.time()))
        time.sleep(sleep_for)


if __name__ == "__main__":
    main()
