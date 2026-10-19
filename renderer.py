import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from dotenv import dotenv_values

from colors import black, light_blue, orange, white
from icon_sets import ICON_RENDERERS, ICON_SET_NAME


WIDTH = 64
HEIGHT = 64
FORECAST_DAYS = 4
FONT_PATH = "3x5pixel.ttf"
DEGREE = chr(176)

BACKGROUND = black
TEXT = white
TEXT_DIM = (150, 164, 180)
GRID = (36, 45, 58)
HOT = orange
COLD = light_blue

WEEKDAYS = ("MO", "TU", "WE", "TH", "FR", "SA", "SU")
TOP_WEEKDAYS = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")

TOP_ROW_Y = 1
TOP_TIME_HOUR_X = 1
TOP_TIME_COLON_X = 9
TOP_TIME_MINUTE_X = 13
TOP_WEEKDAY_CENTER_X = 32
TOP_DATE_RIGHT_X = 62

CURRENT_PANEL_LEFT = 27
CURRENT_PANEL_TOP = 9
CURRENT_PANEL_RIGHT = 62
CURRENT_PANEL_BOTTOM = 32
CURRENT_DETAIL_DIVIDER_X = 45
CURRENT_TEMP_SLOT_TOP = CURRENT_PANEL_TOP
CURRENT_TEMP_SLOT_BOTTOM = 25
CURRENT_TEMP_MAX_WIDTH = CURRENT_PANEL_RIGHT - CURRENT_PANEL_LEFT + 1
CURRENT_TEMP_PIXEL_BIAS_X = 1
CURRENT_TEMP_PIXEL_BIAS_Y = -1
CURRENT_DETAIL_Y = 26
CURRENT_DETAIL_HIGH_LEFT = CURRENT_PANEL_LEFT
CURRENT_DETAIL_HIGH_RIGHT = CURRENT_DETAIL_DIVIDER_X - 1
CURRENT_DETAIL_LOW_LEFT = CURRENT_DETAIL_DIVIDER_X + 1
CURRENT_DETAIL_LOW_RIGHT = CURRENT_PANEL_RIGHT
CURRENT_DETAIL_BOTTOM = CURRENT_DETAIL_Y + 4
CURRENT_DETAIL_MAX_WIDTH = 15
CURRENT_DETAIL_SEPARATOR_GAP = 3

FORECAST_PANEL_TOP = 36
FORECAST_PANEL_BOTTOM = 63
FORECAST_COLUMN_WIDTH = WIDTH // FORECAST_DAYS
FORECAST_ICON_BOX_WIDTH = 12
FORECAST_ICON_BOX_HEIGHT = 10
FORECAST_DAY_Y = 36
FORECAST_ICON_BOX_Y = 42
FORECAST_HIGH_Y = 52
FORECAST_LOW_Y = 58
FORECAST_TEMP_MAX_WIDTH = 14

TINY_FONT = {
    "0": ("###", "#.#", "#.#", "#.#", "###"),
    "1": (".#.", "##.", ".#.", ".#.", "###"),
    "2": ("###", "..#", "###", "#..", "###"),
    "3": ("###", "..#", "###", "..#", "###"),
    "4": ("#.#", "#.#", "###", "..#", "..#"),
    "5": ("###", "#..", "###", "..#", "###"),
    "6": ("###", "#..", "###", "#.#", "###"),
    "7": ("###", "..#", ".#.", ".#.", ".#."),
    "8": ("###", "#.#", "###", "#.#", "###"),
    "9": ("###", "#.#", "###", "..#", "###"),
    "/": ("..#", "..#", ".#.", "#..", "#.."),
    ":": ("...", ".#.", "...", ".#.", "..."),
    "-": ("...", "...", "###", "...", "..."),
    " ": ("...", "...", "...", "...", "..."),
    DEGREE: ("##.", "##.", "...", "...", "..."),
    "A": (".#.", "#.#", "###", "#.#", "#.#"),
    "D": ("##.", "#.#", "#.#", "#.#", "##."),
    "E": ("###", "#..", "###", "#..", "###"),
    "F": ("###", "#..", "###", "#..", "#.."),
    "H": ("#.#", "#.#", "###", "#.#", "#.#"),
    "I": ("###", ".#.", ".#.", ".#.", "###"),
    "M": ("#.#", "###", "###", "#.#", "#.#"),
    "N": ("#.#", "###", "###", "###", "#.#"),
    "O": ("###", "#.#", "#.#", "#.#", "###"),
    "R": ("##.", "#.#", "##.", "#.#", "#.#"),
    "S": ("###", "#..", "###", "..#", "###"),
    "T": ("###", ".#.", ".#.", ".#.", ".#."),
    "U": ("#.#", "#.#", "#.#", "#.#", "###"),
    "W": ("#.#", "#.#", "###", "###", "#.#"),
}

WEATHER_ICON_MAP = {
    # Clear and cloud cover
    0: "clear_sun",
    1: "mostly_sunny",
    2: "partly_cloudy",
    3: "overcast",

    # Fog
    45: "fog",
    48: "rime_fog",

    # Drizzle
    51: "drizzle",
    53: "drizzle",
    55: "drizzle",

    # Freezing drizzle
    56: "freezing_drizzle",
    57: "freezing_drizzle",

    # Rain
    61: "rain",
    63: "rain",
    65: "heavy_rain",

    # Freezing rain
    66: "freezing_rain",
    67: "freezing_rain",

    # Snow
    71: "snow",
    73: "snow",
    77: "snow",
    75: "heavy_snow",

    # Rain showers
    80: "rain_showers",
    81: "rain_showers",
    82: "violent_showers",

    # Snow showers
    85: "snow_showers",
    86: "heavy_snow_showers",

    # Thunderstorms
    95: "thunderstorm",
    96: "hailstorm",
    99: "hailstorm",
}

NIGHT_WEATHER_ICON_MAP = {
    # Only replace sun-bearing current-condition states. Cloud-only and
    # precipitation states remain visually accurate at night.
    0: "clear_moon",
    1: "mostly_clear_night",
    2: "partly_cloudy_night",
}

WEATHER_ICON_RENDERERS = ICON_RENDERERS
ENV = dotenv_values(".env")
TEST_CURRENT_WEATHER_CODE = None
TEST_CURRENT_IS_DAY = None
TEST_FORECAST_WEATHER_CODES = []


def _env_value(name, default=""):
    return str(os.getenv(name, ENV.get(name, default)) or default).strip()


def _env_int(name):
    value = _env_value(name)
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _env_int_list(name):
    values = []
    for raw_value in _env_value(name).split(","):
        raw_value = raw_value.strip()
        if not raw_value:
            continue
        try:
            values.append(int(raw_value))
        except ValueError:
            continue
    return values


TEST_CURRENT_WEATHER_CODE = _env_int("PIXOO_TEST_CURRENT_WEATHER_CODE")
TEST_CURRENT_IS_DAY = _env_int("PIXOO_TEST_CURRENT_IS_DAY")
TEST_FORECAST_WEATHER_CODES = _env_int_list("PIXOO_TEST_FORECAST_WEATHER_CODES")


class ForecastDay:
    def __init__(self, date, code, high, low):
        self.date = date
        self.code = code
        self.high = high
        self.low = low


def render_dashboard(weather_data, blink=False, now=None):
    now = now or datetime.now()
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    font_small = ImageFont.truetype(FONT_PATH, size=5)

    today, forecast = _daily_forecast(weather_data)

    _draw_header(draw, now, blink)
    _draw_current_weather(image, draw, weather_data, today)
    _draw_forecast(image, draw, forecast)

    return image


def _daily_forecast(weather_data):
    daily = weather_data.daily
    days = [
        ForecastDay(
            date=date,
            code=int(daily.weather_code[index]),
            high=round(daily.temperature_2m_max[index]),
            low=round(daily.temperature_2m_min[index]),
        )
        for index, date in enumerate(daily.time)
    ]
    today = days[0]
    return today, days[1:FORECAST_DAYS + 1]


def _draw_header(draw, now, blink):
    draw_top_row(draw, now, blink)
    _draw_hline(draw, 7, GRID)


def draw_top_row(draw, now, blink):
    hour = f"{(now.hour % 12) or 12:02d}"
    minute = now.strftime("%M")
    _draw_pixel_text(draw, TOP_TIME_HOUR_X, TOP_ROW_Y, hour, TEXT)

    if not blink:
        _draw_pixel_text(draw, TOP_TIME_COLON_X, TOP_ROW_Y, ":", TEXT)

    _draw_pixel_text(draw, TOP_TIME_MINUTE_X, TOP_ROW_Y, minute, TEXT)

    weekday = TOP_WEEKDAYS[now.weekday()]
    _draw_pixel_centered_text(draw, TOP_WEEKDAY_CENTER_X, TOP_ROW_Y, weekday, TEXT_DIM)

    date_text = now.strftime("%m/%d")
    _draw_pixel_right_text(draw, TOP_DATE_RIGHT_X, TOP_ROW_Y, date_text, TEXT_DIM)


def _draw_current_weather(image, draw, weather_data, today):
    current_code = int(getattr(weather_data.current, "weather_code", today.code))
    is_day = getattr(weather_data.current, "is_day", None)
    if TEST_CURRENT_WEATHER_CODE is not None:
        current_code = TEST_CURRENT_WEATHER_CODE
    if TEST_CURRENT_IS_DAY is not None:
        is_day = TEST_CURRENT_IS_DAY
    current_icon_key = get_icon_key(current_code, is_day=is_day)
    current_is_night_icon = current_icon_key in NIGHT_WEATHER_ICON_MAP.values()
    current_is_large_icon = current_is_night_icon
    current_icon_scale = 1 if current_is_large_icon else 2
    current_icon_x = 2 if current_is_large_icon else 4
    current_icon_y = 9 if current_is_large_icon else 12
    current_temp = round(weather_data.current.temperature_2m)
    current_temp_text = f"{current_temp}{DEGREE}"
    temp_font = _font_that_fits(draw, current_temp_text, CURRENT_TEMP_MAX_WIDTH, [13, 12, 11, 10, 9, 8])

    _draw_condition_icon(
        image,
        current_code,
        current_icon_x,
        current_icon_y,
        scale=current_icon_scale,
        is_day=is_day,
    )
    _draw_text_centered_in_box(
        draw,
        CURRENT_PANEL_LEFT,
        CURRENT_TEMP_SLOT_TOP,
        CURRENT_PANEL_RIGHT,
        CURRENT_TEMP_SLOT_BOTTOM,
        current_temp_text,
        TEXT,
        temp_font,
        x_bias=CURRENT_TEMP_PIXEL_BIAS_X,
        y_bias=CURRENT_TEMP_PIXEL_BIAS_Y,
    )

    _draw_temperature_near_separator(
        draw,
        CURRENT_DETAIL_HIGH_LEFT,
        CURRENT_DETAIL_Y,
        CURRENT_DETAIL_HIGH_RIGHT,
        CURRENT_DETAIL_BOTTOM,
        CURRENT_DETAIL_DIVIDER_X,
        "left",
        today.high,
        HOT,
        CURRENT_DETAIL_MAX_WIDTH,
    )
    _draw_temperature_near_separator(
        draw,
        CURRENT_DETAIL_LOW_LEFT,
        CURRENT_DETAIL_Y,
        CURRENT_DETAIL_LOW_RIGHT,
        CURRENT_DETAIL_BOTTOM,
        CURRENT_DETAIL_DIVIDER_X,
        "right",
        today.low,
        COLD,
        CURRENT_DETAIL_MAX_WIDTH,
    )
    _draw_vline(draw, CURRENT_DETAIL_DIVIDER_X, CURRENT_DETAIL_Y - 1, CURRENT_PANEL_BOTTOM - 1, GRID)
    _draw_hline(draw, 34, GRID)


def _draw_forecast(image, draw, forecast):
    for index, entry in enumerate(forecast[:FORECAST_DAYS]):
        column_x = index * FORECAST_COLUMN_WIDTH
        center_x = column_x + FORECAST_COLUMN_WIDTH // 2
        weekday = WEEKDAYS[datetime.strptime(entry.date, "%Y-%m-%d").weekday()]
        icon_code = entry.code
        if index < len(TEST_FORECAST_WEATHER_CODES):
            icon_code = TEST_FORECAST_WEATHER_CODES[index]

        _draw_pixel_centered_text(draw, center_x, FORECAST_DAY_Y, weekday, TEXT_DIM)
        _draw_condition_icon_in_box(
            image,
            icon_code,
            center_x - FORECAST_ICON_BOX_WIDTH // 2,
            FORECAST_ICON_BOX_Y,
            FORECAST_ICON_BOX_WIDTH,
            FORECAST_ICON_BOX_HEIGHT,
        )
        _draw_temperature_in_slot(draw, center_x, FORECAST_HIGH_Y, entry.high, TEXT, FORECAST_TEMP_MAX_WIDTH)
        _draw_temperature_in_slot(draw, center_x, FORECAST_LOW_Y, entry.low, TEXT_DIM, FORECAST_TEMP_MAX_WIDTH)

        if index > 0:
            _draw_vline(draw, column_x, FORECAST_DAY_Y, FORECAST_PANEL_BOTTOM - 1, (18, 24, 34))


def _draw_condition_icon(image, code, x, y, scale=1, is_day=None):
    for pixel, color in _condition_pixels(code, x, y, is_day=is_day):
        _put_scaled_pixel(image, pixel, color, scale, (x, y))


def _draw_condition_icon_in_box(image, code, box_x, box_y, box_width, box_height):
    pixels = _condition_pixels(code, 0, 0)
    min_x, min_y, max_x, max_y = _pixel_bounds(pixels)
    icon_width = max_x - min_x + 1
    icon_height = max_y - min_y + 1
    offset_x = box_x + (box_width - icon_width) // 2 - min_x
    offset_y = box_y - min_y

    for (x, y), color in pixels:
        px = x + offset_x
        py = y + offset_y
        if (
            box_x <= px < box_x + box_width
            and box_y <= py < box_y + box_height
            and 0 <= px < WIDTH
            and 0 <= py < HEIGHT
        ):
            image.putpixel((px, py), color)


def get_icon_key(weather_code, is_day=None):
    try:
        code = int(weather_code)
    except (TypeError, ValueError):
        return "weather_unknown"

    try:
        is_night = is_day is not None and int(is_day) == 0
    except (TypeError, ValueError):
        is_night = False

    if is_night:
        return NIGHT_WEATHER_ICON_MAP.get(code, WEATHER_ICON_MAP.get(code, "weather_unknown"))

    return WEATHER_ICON_MAP.get(code, "weather_unknown")


def _condition_pixels(code, x, y, is_day=None):
    icon_key = get_icon_key(code, is_day=is_day)
    return WEATHER_ICON_RENDERERS[icon_key](x, y)


def _pixel_bounds(pixels):
    xs = [coordinate[0] for coordinate, color in pixels]
    ys = [coordinate[1] for coordinate, color in pixels]
    return min(xs), min(ys), max(xs), max(ys)


def _put_scaled_pixel(image, coordinate, color, scale, origin):
    x, y = coordinate
    origin_x, origin_y = origin
    for dx in range(scale):
        for dy in range(scale):
            px = origin_x + (x - origin_x) * scale + dx
            py = origin_y + (y - origin_y) * scale + dy
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                image.putpixel((px, py), color)


def _draw_pixel_text(draw, x, y, text, fill):
    cursor_x = x
    for character in text:
        glyph = TINY_FONT.get(character.upper(), TINY_FONT[" "])
        for row, pixels in enumerate(glyph):
            for column, pixel in enumerate(pixels):
                if pixel == "#":
                    draw.point((cursor_x + column, y + row), fill=fill)
        cursor_x += len(glyph[0]) + 1


def _pixel_text_width(text):
    width = 0
    for character in text:
        glyph = TINY_FONT.get(character.upper(), TINY_FONT[" "])
        width += len(glyph[0]) + 1
    return max(0, width - 1)


def _draw_pixel_centered_text(draw, center_x, y, text, fill):
    _draw_pixel_text(draw, center_x - _pixel_text_width(text) // 2, y, text, fill)


def _draw_pixel_right_text(draw, right_x, y, text, fill):
    _draw_pixel_text(draw, right_x - _pixel_text_width(text) + 1, y, text, fill)


def _draw_temperature_in_slot(draw, center_x, y, value, fill, max_width):
    text = _temperature_text(value, max_width)
    _draw_pixel_text_centered_on_point(draw, center_x, y, text, fill)


def _draw_temperature_in_box(draw, left, top, right, bottom, value, fill, max_width):
    text = _temperature_text(value, max_width)
    _draw_pixel_text_centered_in_box(draw, left, top, right, bottom, text, fill)


def _draw_temperature_near_separator(draw, left, top, right, bottom, separator_x, side, value, fill, max_width):
    text = _temperature_text(value, max_width)
    _draw_pixel_text_near_separator(
        draw,
        left,
        top,
        right,
        bottom,
        separator_x,
        side,
        CURRENT_DETAIL_SEPARATOR_GAP,
        text,
        fill,
    )


def _temperature_text(value, max_width):
    value = round(value)
    with_degree = f"{value}{DEGREE}"
    if _pixel_text_width(with_degree) <= max_width:
        return with_degree

    without_degree = str(value)
    if _pixel_text_width(without_degree) <= max_width:
        return without_degree

    return "--"


def _draw_pixel_text_centered_in_box(draw, left, top, right, bottom, text, fill):
    lit_pixels = _pixel_text_lit_pixels(text)
    if not lit_pixels:
        return

    min_x = min(x for x, y in lit_pixels)
    max_x = max(x for x, y in lit_pixels)
    min_y = min(y for x, y in lit_pixels)
    max_y = max(y for x, y in lit_pixels)
    box_width = right - left + 1
    box_height = bottom - top + 1
    lit_width = max_x - min_x + 1
    lit_height = max_y - min_y + 1
    target_x = left + (box_width - lit_width) // 2
    target_y = top + (box_height - lit_height) // 2

    for source_x, source_y in lit_pixels:
        draw.point((target_x + source_x - min_x, target_y + source_y - min_y), fill=fill)


def _draw_pixel_text_centered_on_point(draw, center_x, y, text, fill):
    lit_pixels = _pixel_text_lit_pixels(text)
    if not lit_pixels:
        return

    min_x = min(x for x, y in lit_pixels)
    max_x = max(x for x, y in lit_pixels)
    lit_width = max_x - min_x + 1
    target_x = center_x - lit_width // 2

    for source_x, source_y in lit_pixels:
        draw.point((target_x + source_x - min_x, y + source_y), fill=fill)


def _draw_pixel_text_near_separator(draw, left, top, right, bottom, separator_x, side, gap, text, fill):
    lit_pixels = _pixel_text_lit_pixels(text)
    if not lit_pixels:
        return

    min_x = min(x for x, y in lit_pixels)
    max_x = max(x for x, y in lit_pixels)
    min_y = min(y for x, y in lit_pixels)
    max_y = max(y for x, y in lit_pixels)
    box_height = bottom - top + 1
    lit_width = max_x - min_x + 1
    lit_height = max_y - min_y + 1
    target_y = top + (box_height - lit_height) // 2

    if side == "left":
        target_x = separator_x - gap - lit_width
        target_x = max(left, min(target_x, right - lit_width + 1))
    else:
        target_x = separator_x + gap + 1
        target_x = max(left, min(target_x, right - lit_width + 1))

    for source_x, source_y in lit_pixels:
        draw.point((target_x + source_x - min_x, target_y + source_y - min_y), fill=fill)


def _pixel_text_lit_pixels(text):
    lit_pixels = []
    cursor_x = 0
    for character in text:
        glyph = TINY_FONT.get(character.upper(), TINY_FONT[" "])
        for row, pixels in enumerate(glyph):
            for column, pixel in enumerate(pixels):
                if pixel == "#":
                    lit_pixels.append((cursor_x + column, row))
        cursor_x += len(glyph[0]) + 1

    return lit_pixels


def _draw_centered_text(draw, position, text, fill, font):
    x, y = position
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text((x - (bbox[2] - bbox[0]) // 2, y), text, fill, font=font)


def _draw_text_centered_in_box(draw, left, top, right, bottom, text, fill, font, x_bias=0, y_bias=0):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    if text_width <= 0 or text_height <= 0:
        return

    scratch = Image.new("RGB", (text_width, text_height), BACKGROUND)
    scratch_draw = ImageDraw.Draw(scratch)
    scratch_draw.text((-bbox[0], -bbox[1]), text, fill, font=font)

    lit_pixels = [
        (x, y)
        for y in range(text_height)
        for x in range(text_width)
        if scratch.getpixel((x, y)) != BACKGROUND
    ]
    if not lit_pixels:
        return

    min_x = min(x for x, y in lit_pixels)
    max_x = max(x for x, y in lit_pixels)
    min_y = min(y for x, y in lit_pixels)
    max_y = max(y for x, y in lit_pixels)

    box_width = right - left + 1
    box_height = bottom - top + 1
    lit_width = max_x - min_x + 1
    lit_height = max_y - min_y + 1
    target_x = left + (box_width - lit_width) // 2 + x_bias
    target_y = top + (box_height - lit_height) // 2 + y_bias

    for source_x, source_y in lit_pixels:
        draw.point(
            (target_x + source_x - min_x, target_y + source_y - min_y),
            fill=scratch.getpixel((source_x, source_y)),
        )


def _draw_right_text(draw, position, text, fill, font):
    x, y = position
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text((x - (bbox[2] - bbox[0]), y), text, fill, font=font)


def _font_that_fits(draw, text, max_width, sizes):
    for size in sizes:
        font = ImageFont.truetype(FONT_PATH, size=size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font

    return ImageFont.truetype(FONT_PATH, size=sizes[-1])


def _draw_hline(draw, y, fill):
    draw.line((0, y, WIDTH - 1, y), fill=fill)


def _draw_vline(draw, x, y1, y2, fill):
    draw.line((x, y1, x, y2), fill=fill)
