from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from renderer import (
    BACKGROUND,
    FONT_PATH,
    FORECAST_ICON_BOX_HEIGHT,
    FORECAST_ICON_BOX_WIDTH,
    GRID,
    NIGHT_WEATHER_ICON_MAP,
    TEXT,
    TEXT_DIM,
    _condition_pixels,
    get_icon_key,
)


MOCKUP_DIR = Path("mockups")
SCALE = 8

WEATHER_CODES = [
    (0, "clear"),
    (1, "mainly clear"),
    (2, "partly cloudy"),
    (3, "overcast"),
    (45, "fog"),
    (48, "rime fog"),
    (51, "drizzle"),
    (56, "freezing drizzle"),
    (61, "rain"),
    (65, "heavy rain"),
    (66, "freezing rain"),
    (71, "snow"),
    (75, "heavy snow"),
    (77, "snow"),
    (80, "rain showers"),
    (82, "violent showers"),
    (85, "snow showers"),
    (86, "heavy snow showers"),
    (95, "thunderstorm"),
    (96, "hailstorm"),
    (68, "fallback"),
]

CURRENT_NIGHT_CODES = [
    (0, "clear night"),
    (1, "mainly clear night"),
    (2, "partly cloudy night"),
]


def draw_label(draw, font, x, y, text, fill=TEXT_DIM):
    draw.text((x, y), text.upper()[:14], fill=fill, font=font)


def compact_key(code, is_day):
    key = get_icon_key(code, is_day=is_day)
    return key.replace("_", " ")


def draw_current_icon(image, code, x, y, is_day=None):
    icon_key = get_icon_key(code, is_day=is_day)
    is_night_icon = icon_key in NIGHT_WEATHER_ICON_MAP.values()
    scale = 1 if is_night_icon else 2
    pixels = _condition_pixels(code, x, y, is_day=is_day)
    for (px, py), color in pixels:
        for dx in range(scale):
            for dy in range(scale):
                target_x = x + (px - x) * scale + dx
                target_y = y + (py - y) * scale + dy
                if 0 <= target_x < image.width and 0 <= target_y < image.height:
                    image.putpixel((target_x, target_y), color)


def draw_forecast_icon_in_box(image, code, box_x, box_y):
    pixels = _condition_pixels(code, 0, 0)
    min_x = min(pixel[0][0] for pixel in pixels)
    min_y = min(pixel[0][1] for pixel in pixels)
    max_x = max(pixel[0][0] for pixel in pixels)
    max_y = max(pixel[0][1] for pixel in pixels)
    icon_width = max_x - min_x + 1
    icon_height = max_y - min_y + 1
    offset_x = box_x + (FORECAST_ICON_BOX_WIDTH - icon_width) // 2 - min_x
    offset_y = box_y - min_y

    for (px, py), color in pixels:
        target_x = px + offset_x
        target_y = py + offset_y
        if (
            box_x <= target_x < box_x + FORECAST_ICON_BOX_WIDTH
            and box_y <= target_y < box_y + FORECAST_ICON_BOX_HEIGHT
            and 0 <= target_x < image.width
            and 0 <= target_y < image.height
        ):
            image.putpixel((target_x, target_y), color)


def draw_preview_sheet(items, filename, draw_icon):
    columns = 4
    cell = 64
    rows = (len(items) + columns - 1) // columns
    image = Image.new("RGB", (columns * cell, rows * cell), BACKGROUND)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, size=5)

    for index, item in enumerate(items):
        code, _label, is_day = item
        column = index % columns
        row = index // columns
        x = column * cell
        y = row * cell
        draw.rectangle((x, y, x + cell - 1, y + cell - 1), outline=GRID)
        draw_label(draw, font, x + 2, y + 2, str(code))
        draw_label(draw, font, x + 2, y + 52, compact_key(code, is_day), TEXT)
        draw_icon(image, code, x, y, is_day)

    output_path = MOCKUP_DIR / filename
    image.resize((image.width * SCALE, image.height * SCALE), Image.Resampling.NEAREST).save(output_path)
    return output_path


def main():
    MOCKUP_DIR.mkdir(exist_ok=True)

    current_items = [(code, label, None) for code, label in WEATHER_CODES]
    current_items.extend((code, label, 0) for code, label in CURRENT_NIGHT_CODES)
    forecast_items = [(code, label, None) for code, label in WEATHER_CODES]

    current_path = draw_preview_sheet(
        current_items,
        "function-current-icon-baseline.png",
        lambda image, code, x, y, is_day: draw_current_icon(image, code, x + 20, y + 16, is_day),
    )
    forecast_path = draw_preview_sheet(
        forecast_items,
        "function-forecast-icon-baseline.png",
        lambda image, code, x, y, is_day: draw_forecast_icon_in_box(image, code, x + 26, y + 24),
    )

    print(current_path)
    print(forecast_path)


if __name__ == "__main__":
    main()
