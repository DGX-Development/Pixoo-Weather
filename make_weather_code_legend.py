from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from renderer import _condition_pixels, get_icon_key


SLIDE_DIR = Path("weather-code-slides")
FONT_PATH = "3x5pixel.ttf"
BASE_SIZE = 64
SCALE = 8
BACKGROUND = (0, 0, 0)
TEXT = (255, 255, 255)
TEXT_DIM = (150, 164, 180)
GRID = (36, 45, 58)

WEATHER_CODES = [
    (0, "clear sky"),
    (1, "mainly clear"),
    (2, "partly cloudy"),
    (3, "overcast"),
    (45, "fog"),
    (48, "depositing rime fog"),
    (51, "light drizzle"),
    (53, "moderate drizzle"),
    (55, "dense drizzle"),
    (56, "light freezing drizzle"),
    (57, "dense freezing drizzle"),
    (61, "slight rain"),
    (63, "moderate rain"),
    (65, "heavy rain"),
    (66, "light freezing rain"),
    (67, "heavy freezing rain"),
    (71, "slight snow"),
    (73, "moderate snow"),
    (75, "heavy snow"),
    (77, "snow grains"),
    (80, "slight rain showers"),
    (81, "moderate rain showers"),
    (82, "violent rain showers"),
    (85, "slight snow showers"),
    (86, "heavy snow showers"),
    (95, "thunderstorm"),
    (96, "thunderstorm with slight hail"),
    (99, "thunderstorm with heavy hail"),
    (68, "unexpected code example"),
]

NIGHT_WEATHER_CODES = [
    (0, "clear sky at night"),
    (1, "mainly clear at night"),
    (2, "partly cloudy at night"),
]


def draw_pixel_text(draw, font, x, y, text, fill):
    draw.text((x, y), text.upper(), fill=fill, font=font)


def draw_icon(image, code, box, is_day=None):
    box_x, box_y, box_width, box_height = box
    pixels = _condition_pixels(code, 0, 0, is_day=is_day)
    min_x = min(pixel[0][0] for pixel in pixels)
    min_y = min(pixel[0][1] for pixel in pixels)
    max_x = max(pixel[0][0] for pixel in pixels)
    max_y = max(pixel[0][1] for pixel in pixels)
    icon_width = max_x - min_x + 1
    icon_height = max_y - min_y + 1
    offset_x = box_x + (box_width - icon_width) // 2 - min_x
    offset_y = box_y + (box_height - icon_height) // 2 - min_y

    for (px, py), color in pixels:
        x = px + offset_x
        y = py + offset_y
        if 0 <= x < image.width and 0 <= y < image.height:
            image.putpixel((x, y), color)


def make_slide(code, condition, icon_name, is_day=None):
    image = Image.new("RGB", (BASE_SIZE, BASE_SIZE), BACKGROUND)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, size=5)

    code_text = f"CODE {code}"
    draw_pixel_text(draw, font, 2, 2, code_text, TEXT)
    draw.line((0, 9, BASE_SIZE - 1, 9), fill=GRID)

    draw_icon(image, code, (20, 15, 24, 24), is_day=is_day)

    draw.line((0, 43, BASE_SIZE - 1, 43), fill=GRID)
    draw_pixel_text(draw, font, 2, 51, short_icon_name(icon_name), TEXT)

    suffix = "-night" if is_day == 0 else ""
    filename = f"code-{code}{suffix}.png"
    large_path = SLIDE_DIR / filename.replace(".png", "-512.png")
    image.resize((BASE_SIZE * SCALE, BASE_SIZE * SCALE), Image.Resampling.NEAREST).save(large_path)
    return large_path.as_posix()


def short_icon_name(icon_name):
    return icon_name.replace("_", " ").upper()[:15]


def write_preview(slides):
    slide_objects = ",\n      ".join(
        "{"
        f"src: '{path}', "
        f"code: '{code}', "
        f"condition: '{condition}', "
        f"icon: '{icon_name}'"
        "}"
        for code, condition, icon_name, path in slides
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Open-Meteo Icon Slideshow</title>
  <style>
    :root {{
      color-scheme: dark;
      font-family: Arial, sans-serif;
      background: #111;
      color: #eee;
    }}
    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
    }}
    main {{
      width: min(92vmin, 760px);
    }}
    img {{
      display: block;
      width: 100%;
      aspect-ratio: 1 / 1;
      image-rendering: pixelated;
      image-rendering: crisp-edges;
      background: #000;
    }}
    .meta {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      margin-top: 12px;
      color: #bbb;
      font-size: 16px;
    }}
    .controls {{
      display: flex;
      gap: 12px;
      margin-top: 12px;
    }}
    button {{
      flex: 1;
      padding: 12px;
      border: 1px solid #444;
      background: #1f2933;
      color: #fff;
      font-size: 16px;
      cursor: pointer;
    }}
    .sheet {{
      margin-top: 32px;
    }}
  </style>
</head>
<body>
  <main>
    <img id="slide" src="" alt="Weather code icon slide">
    <div class="meta">
      <span id="title"></span>
      <span id="count"></span>
    </div>
    <div class="meta">
      <span id="icon"></span>
    </div>
    <div class="controls">
      <button id="prev" type="button">Previous</button>
      <button id="next" type="button">Next</button>
    </div>
    <img class="sheet" src="weather-icon-key-sheet-large.png" alt="All supported weather icon keys">
  </main>
  <script>
    const slides = [
      {slide_objects}
    ];
    let index = 0;
    const image = document.getElementById('slide');
    const title = document.getElementById('title');
    const count = document.getElementById('count');
    const icon = document.getElementById('icon');

    function showSlide() {{
      const slide = slides[index];
      image.src = slide.src;
      title.textContent = `Code ${{slide.code}}: ${{slide.condition}}`;
      icon.textContent = slide.icon;
      count.textContent = `${{index + 1}} / ${{slides.length}}`;
    }}

    document.getElementById('prev').addEventListener('click', () => {{
      index = (index - 1 + slides.length) % slides.length;
      showSlide();
    }});
    document.getElementById('next').addEventListener('click', () => {{
      index = (index + 1) % slides.length;
      showSlide();
    }});
    document.addEventListener('keydown', (event) => {{
      if (event.key === 'ArrowLeft') document.getElementById('prev').click();
      if (event.key === 'ArrowRight') document.getElementById('next').click();
    }});
    showSlide();
  </script>
</body>
</html>
"""
    Path("preview.html").write_text(html, encoding="utf-8")


def make_icon_key_sheet():
    unique_keys = []
    for code, condition in WEATHER_CODES:
        icon_key = get_icon_key(code)
        if icon_key not in unique_keys:
            unique_keys.append(icon_key)
    for code, condition in NIGHT_WEATHER_CODES:
        icon_key = get_icon_key(code, is_day=0)
        if icon_key not in unique_keys:
            unique_keys.append(icon_key)

    columns = 4
    cell = 64
    rows = (len(unique_keys) + columns - 1) // columns
    image = Image.new("RGB", (columns * cell, rows * cell), BACKGROUND)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, size=5)
    sample_by_key = {get_icon_key(code): (code, None) for code, condition in WEATHER_CODES}
    for code, condition in NIGHT_WEATHER_CODES:
        sample_by_key[get_icon_key(code, is_day=0)] = (code, 0)

    for index, icon_key in enumerate(unique_keys):
        column = index % columns
        row = index // columns
        x = column * cell
        y = row * cell
        draw.rectangle((x, y, x + cell - 1, y + cell - 1), outline=GRID)
        draw_pixel_text(draw, font, x + 2, y + 2, short_icon_name(icon_key), TEXT_DIM)
        sample_code, is_day = sample_by_key[icon_key]
        draw_icon(image, sample_code, (x + 20, y + 18, 24, 24), is_day=is_day)

    image.resize((image.width * 3, image.height * 3), Image.Resampling.NEAREST).save(
        "weather-icon-key-sheet-large.png"
    )


def main():
    SLIDE_DIR.mkdir(exist_ok=True)
    slides = []
    for code, condition in WEATHER_CODES:
        icon_name = get_icon_key(code)
        path = make_slide(code, condition, icon_name)
        slides.append((code, condition, icon_name, path))
    for code, condition in NIGHT_WEATHER_CODES:
        icon_name = get_icon_key(code, is_day=0)
        path = make_slide(code, condition, icon_name, is_day=0)
        slides.append((f"{code} night", condition, icon_name, path))
    make_icon_key_sheet()
    write_preview(slides)


if __name__ == "__main__":
    main()
