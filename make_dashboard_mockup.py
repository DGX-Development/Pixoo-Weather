from datetime import datetime
import json
from pathlib import Path

from PIL import Image

from renderer import (
    BACKGROUND,
    FORECAST_ICON_BOX_HEIGHT,
    FORECAST_ICON_BOX_WIDTH,
    NIGHT_WEATHER_ICON_MAP,
    _condition_pixels,
    get_icon_key,
    render_dashboard,
)
from weatherresponse import Current, CurrentUnits, Daily, DailyUnits, WeatherResponse


MOCKUP_DIR = Path("mockups")
MOCKUP_IMAGE = MOCKUP_DIR / "dashboard-current.png"
EDITOR_HTML = MOCKUP_DIR / "dashboard-editor.html"

PALETTE = [
    ("off", (0, 0, 0)),
    ("white", (255, 255, 255)),
    ("blue", (0, 102, 255)),
    ("rain", (18, 212, 255)),
    ("cyan", (13, 255, 241)),
    ("yellow", (255, 255, 13)),
    ("orange", (255, 168, 0)),
    ("moon", (255, 214, 80)),
    ("moon hi", (255, 238, 140)),
    ("moon edge", (210, 150, 40)),
    ("gray", (170, 180, 194)),
    ("gray dark", (82, 91, 105)),
]

WEATHER_ICON_ITEMS = [
    ("0", "clear sky", 0, None),
    ("1", "mainly clear", 1, None),
    ("2", "partly cloudy", 2, None),
    ("3", "overcast", 3, None),
    ("45", "fog", 45, None),
    ("48", "rime fog", 48, None),
    ("51/53/55", "drizzle", 51, None),
    ("56/57", "freezing drizzle", 56, None),
    ("61/63", "rain", 61, None),
    ("65", "heavy rain", 65, None),
    ("66/67", "freezing rain", 66, None),
    ("71/73/77", "snow", 71, None),
    ("75", "heavy snow", 75, None),
    ("80/81", "rain showers", 80, None),
    ("82", "violent showers", 82, None),
    ("85", "snow showers", 85, None),
    ("86", "heavy snow showers", 86, None),
    ("95", "thunderstorm", 95, None),
    ("96/99", "hailstorm", 96, None),
    ("unknown", "weather unknown", 68, None),
]

CURRENT_NIGHT_ICON_ITEMS = [
    ("0 night", "clear night", 0, 0),
    ("1 night", "mainly clear night", 1, 0),
    ("2 night", "partly cloudy night", 2, 0),
]


def sample_weather(current_temp=68.8):
    return WeatherResponse(
        latitude=40.7128,
        longitude=-74.0060,
        generationtime_ms=0,
        utc_offset_seconds=-18000,
        timezone="America/New_York",
        timezone_abbreviation="EST",
        elevation=251,
        current_units=CurrentUnits(
            time="iso8601",
            interval="seconds",
            temperature_2m="F",
            weather_code="wmo code",
            is_day="",
        ),
        current=Current(
            time="2026-05-29T23:00",
            interval=900,
            temperature_2m=current_temp,
            weather_code=3,
            is_day=0,
        ),
        daily_units=DailyUnits(
            time="iso8601",
            weather_code="wmo code",
            temperature_2m_max="F",
            temperature_2m_min="F",
        ),
        daily=Daily(
            time=["2026-05-29", "2026-05-30", "2026-05-31", "2026-06-01", "2026-06-02"],
            weather_code=[3, 3, 55, 51, 53],
            temperature_2m_max=[83.2, 85.8, 75.6, 79.7, 75.8],
            temperature_2m_min=[57.1, 62.6, 57.1, 55.6, 57.1],
        ),
    )


def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(*color)


def image_pixels(image):
    return [rgb_to_hex(image.getpixel((x, y))) for y in range(image.height) for x in range(image.width)]


def put_pixel(image, x, y, color):
    if 0 <= x < image.width and 0 <= y < image.height:
        image.putpixel((x, y), color)


def draw_current_icon_image(code, is_day):
    icon_key = get_icon_key(code, is_day=is_day)
    is_night_icon = icon_key in NIGHT_WEATHER_ICON_MAP.values()
    scale = 1 if is_night_icon else 2
    image = Image.new("RGB", (24, 24), BACKGROUND)

    for (px, py), color in _condition_pixels(code, 0, 0, is_day=is_day):
        for dx in range(scale):
            for dy in range(scale):
                put_pixel(image, px * scale + dx, py * scale + dy, color)

    return image


def draw_forecast_icon_image(code):
    image = Image.new("RGB", (FORECAST_ICON_BOX_WIDTH, FORECAST_ICON_BOX_HEIGHT), BACKGROUND)
    pixels = _condition_pixels(code, 0, 0)
    min_x = min(pixel[0][0] for pixel in pixels)
    min_y = min(pixel[0][1] for pixel in pixels)
    max_x = max(pixel[0][0] for pixel in pixels)
    max_y = max(pixel[0][1] for pixel in pixels)
    icon_width = max_x - min_x + 1
    icon_height = max_y - min_y + 1
    offset_x = (FORECAST_ICON_BOX_WIDTH - icon_width) // 2 - min_x
    offset_y = -min_y

    for (px, py), color in pixels:
        put_pixel(image, px + offset_x, py + offset_y, color)

    return image


def make_icon_payload(items, size, renderer):
    icons = []
    seen = set()
    for codes, label, code, is_day in items:
        icon_key = get_icon_key(code, is_day=is_day)
        item_id = f"{codes}-{icon_key}"
        if item_id in seen:
            continue
        seen.add(item_id)

        image = renderer(code, is_day) if renderer == draw_current_icon_image else renderer(code)
        icons.append(
            {
                "id": item_id,
                "codes": codes,
                "label": label,
                "key": icon_key,
                "width": size[0],
                "height": size[1],
                "pixels": image_pixels(image),
            }
        )
    return icons


def write_editor(dashboard_images):
    dashboard_cases = []
    for label, filename in dashboard_images:
        image = Image.open(MOCKUP_DIR / filename).convert("RGB")
        dashboard_cases.append(
            {
                "id": filename,
                "label": label,
                "width": image.width,
                "height": image.height,
                "pixels": image_pixels(image),
            }
        )

    data = {
        "dashboardCases": dashboard_cases,
        "currentIcons": make_icon_payload(
            WEATHER_ICON_ITEMS + CURRENT_NIGHT_ICON_ITEMS,
            (24, 24),
            draw_current_icon_image,
        ),
        "forecastIcons": make_icon_payload(
            WEATHER_ICON_ITEMS,
            (FORECAST_ICON_BOX_WIDTH, FORECAST_ICON_BOX_HEIGHT),
            draw_forecast_icon_image,
        ),
        "palette": [{"name": name, "color": rgb_to_hex(color)} for name, color in PALETTE],
    }

    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pixoo Pixel Editor</title>
  <style>
    :root {
      color-scheme: dark;
      background: #0b0d10;
      color: #e8edf5;
      font-family: Segoe UI, Arial, sans-serif;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      background: #0b0d10;
    }

    main {
      width: min(96vw, 1120px);
      margin: 16px auto;
      display: grid;
      gap: 12px;
    }

    header,
    .toolbar,
    .palette,
    .actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    header {
      justify-content: space-between;
    }

    h1 {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
    }

    button,
    select {
      height: 32px;
      border: 1px solid #273041;
      background: #111722;
      color: #e8edf5;
      padding: 0 10px;
      font: inherit;
    }

    button {
      cursor: pointer;
    }

    button.active {
      border-color: #7dd3fc;
      background: #163042;
    }

    .panel {
      border: 1px solid #273041;
      background: #0f141d;
      padding: 12px;
      display: grid;
      gap: 12px;
    }

    .editor-row {
      display: grid;
      grid-template-columns: auto minmax(220px, 1fr);
      gap: 16px;
      align-items: start;
    }

    .canvas-shell {
      position: relative;
      width: min(84vmin, 720px);
      background: #000;
      border: 1px solid #273041;
      cursor: crosshair;
    }

    .canvas-shell.icon {
      width: min(84vmin, 520px);
    }

    canvas {
      display: block;
      width: 100%;
      height: auto;
      image-rendering: pixelated;
      image-rendering: crisp-edges;
      user-select: none;
      touch-action: none;
    }

    .grid {
      position: absolute;
      inset: 0;
      pointer-events: none;
      background-image:
        linear-gradient(rgba(255,255,255,.2) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.2) 1px, transparent 1px);
      background-size: calc(100% / var(--grid-w)) calc(100% / var(--grid-h));
    }

    .side {
      display: grid;
      gap: 12px;
      min-width: 240px;
    }

    .readout {
      min-height: 22px;
      font: 13px Consolas, monospace;
      color: #dbeafe;
    }

    .swatch {
      width: 30px;
      height: 30px;
      padding: 0;
      border: 2px solid #273041;
    }

    .swatch.active {
      border-color: #fff;
      box-shadow: 0 0 0 2px #000, 0 0 0 4px #7dd3fc;
    }

    .hint {
      margin: 0;
      color: #9aa8ba;
      font-size: 13px;
      line-height: 1.4;
    }

    @media (max-width: 820px) {
      .editor-row {
        grid-template-columns: 1fr;
      }

      .canvas-shell,
      .canvas-shell.icon {
        width: 100%;
      }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Pixoo Pixel Editor</h1>
      <div class="toolbar" role="tablist" aria-label="Editor mode">
        <button id="dashboardMode" class="active" type="button">Dashboard</button>
        <button id="currentMode" type="button">Current Icon</button>
        <button id="forecastMode" type="button">Forecast Icon</button>
      </div>
    </header>

    <section class="panel">
      <div class="toolbar">
        <label id="dashboardControl">
          Dashboard
          <select id="dashboardSelect"></select>
        </label>
        <label id="iconControl" hidden>
          Icon
          <select id="iconSelect"></select>
        </label>
      </div>

      <div class="palette" id="palette" aria-label="Paint colors"></div>

      <div class="editor-row">
        <div class="canvas-shell" id="canvasShell">
          <canvas id="editorCanvas" width="64" height="64"></canvas>
          <div class="grid" id="grid"></div>
        </div>
        <aside class="side">
          <div class="readout" id="readout">select a color, then click a pixel</div>
          <div class="actions">
            <button id="autoIconsButton" type="button">Auto-Populate Icons</button>
            <button id="resetButton" type="button">Reset Selection</button>
            <button id="downloadButton" type="button">Download PNG</button>
            <button id="copyButton" type="button">Copy JSON</button>
          </div>
          <p class="hint">
            Click or drag inside the enlarged grid to paint with the active
            palette color. Edits stay in this browser session until you export
            them; source icons are not changed automatically.
          </p>
        </aside>
      </div>
    </section>
  </main>

  <script>
    const DATA = __EDITOR_DATA__;
    const canvas = document.getElementById("editorCanvas");
    const ctx = canvas.getContext("2d");
    const shell = document.getElementById("canvasShell");
    const grid = document.getElementById("grid");
    const readout = document.getElementById("readout");
    const palette = document.getElementById("palette");
    const dashboardSelect = document.getElementById("dashboardSelect");
    const iconSelect = document.getElementById("iconSelect");
    const dashboardControl = document.getElementById("dashboardControl");
    const iconControl = document.getElementById("iconControl");
    const modeButtons = {
      dashboard: document.getElementById("dashboardMode"),
      current: document.getElementById("currentMode"),
      forecast: document.getElementById("forecastMode")
    };

    let mode = "dashboard";
    let activeColor = DATA.palette[0].color;
    let activePixels = [];
    let originalPixels = [];
    let activeWidth = 64;
    let activeHeight = 64;
    let painting = false;
    let loadedItem = null;
    const BACKGROUND = "#000000";
    const CURRENT_ICON_CLEAR = { x: 0, y: 8, width: 27, height: 25 };
    const CURRENT_ICON_DAY_POSITION = { x: 4, y: 12 };
    const CURRENT_ICON_NIGHT_POSITION = { x: 2, y: 9 };
    const NIGHT_ICON_KEYS = new Set(["clear_moon", "clear_night", "mostly_clear_night", "partly_cloudy_night"]);
    const FORECAST_ICON_BOXES = [
      { x: 2, y: 42, width: 12, height: 10 },
      { x: 18, y: 42, width: 12, height: 10 },
      { x: 34, y: 42, width: 12, height: 10 },
      { x: 50, y: 42, width: 12, height: 10 }
    ];

    function clonePixels(pixels) {
      return pixels.slice();
    }

    function optionText(item) {
      if (item.codes) return `${item.codes} - ${item.label} (${item.key})`;
      return item.label;
    }

    function setOptions(select, items) {
      select.innerHTML = "";
      for (const item of items) {
        const option = document.createElement("option");
        option.value = item.id;
        option.textContent = optionText(item);
        select.appendChild(option);
      }
    }

    function activeCollection() {
      if (mode === "dashboard") return DATA.dashboardCases;
      if (mode === "current") return DATA.currentIcons;
      return DATA.forecastIcons;
    }

    function activeId() {
      return mode === "dashboard" ? dashboardSelect.value : iconSelect.value;
    }

    function activeItem() {
      return activeCollection().find((item) => item.id === activeId());
    }

    function setMode(nextMode) {
      saveActivePixels();
      mode = nextMode;
      for (const [key, button] of Object.entries(modeButtons)) {
        button.classList.toggle("active", key === mode);
      }

      dashboardControl.hidden = mode !== "dashboard";
      iconControl.hidden = mode === "dashboard";
      shell.classList.toggle("icon", mode !== "dashboard");

      if (mode === "dashboard") {
        loadItem(DATA.dashboardCases[0]);
      } else {
        setOptions(iconSelect, activeCollection());
        loadItem(activeCollection()[0]);
      }
    }

    function setCanvasSize(width, height) {
      activeWidth = width;
      activeHeight = height;
      canvas.width = width;
      canvas.height = height;
      grid.style.setProperty("--grid-w", width);
      grid.style.setProperty("--grid-h", height);
    }

    function loadItem(item) {
      loadedItem = item;
      if (!item.originalPixels) item.originalPixels = clonePixels(item.pixels);
      setCanvasSize(item.width, item.height);
      activePixels = clonePixels(item.pixels);
      originalPixels = clonePixels(item.originalPixels);
      drawPixels();
      readout.textContent = `${item.label || item.key}: ${item.width} x ${item.height}`;
    }

    function saveActivePixels() {
      if (loadedItem && activePixels.length) loadedItem.pixels = clonePixels(activePixels);
    }

    function drawPixels() {
      const imageData = ctx.createImageData(activeWidth, activeHeight);
      for (let index = 0; index < activePixels.length; index += 1) {
        const color = activePixels[index];
        const offset = index * 4;
        imageData.data[offset] = parseInt(color.slice(1, 3), 16);
        imageData.data[offset + 1] = parseInt(color.slice(3, 5), 16);
        imageData.data[offset + 2] = parseInt(color.slice(5, 7), 16);
        imageData.data[offset + 3] = 255;
      }
      ctx.putImageData(imageData, 0, 0);
    }

    function paintAt(event) {
      const rect = canvas.getBoundingClientRect();
      const x = Math.min(activeWidth - 1, Math.max(0, Math.floor(((event.clientX - rect.left) / rect.width) * activeWidth)));
      const y = Math.min(activeHeight - 1, Math.max(0, Math.floor(((event.clientY - rect.top) / rect.height) * activeHeight)));
      const index = y * activeWidth + x;
      activePixels[index] = activeColor;
      ctx.fillStyle = activeColor;
      ctx.fillRect(x, y, 1, 1);
      readout.textContent = `x=${x}, y=${y}, color=${activeColor}`;
    }

    function pixelIndex(x, y) {
      return y * activeWidth + x;
    }

    function fillPixels(x, y, width, height, color) {
      for (let py = y; py < y + height; py += 1) {
        for (let px = x; px < x + width; px += 1) {
          if (px >= 0 && py >= 0 && px < activeWidth && py < activeHeight) {
            activePixels[pixelIndex(px, py)] = color;
          }
        }
      }
    }

    function pasteIcon(icon, x, y) {
      for (let py = 0; py < icon.height; py += 1) {
        for (let px = 0; px < icon.width; px += 1) {
          const color = icon.pixels[py * icon.width + px];
          const targetX = x + px;
          const targetY = y + py;
          if (
            color !== BACKGROUND &&
            targetX >= 0 &&
            targetY >= 0 &&
            targetX < activeWidth &&
            targetY < activeHeight
          ) {
            activePixels[pixelIndex(targetX, targetY)] = color;
          }
        }
      }
    }

    function shuffled(items) {
      const copy = items.slice();
      for (let index = copy.length - 1; index > 0; index -= 1) {
        const swapIndex = Math.floor(Math.random() * (index + 1));
        [copy[index], copy[swapIndex]] = [copy[swapIndex], copy[index]];
      }
      return copy;
    }

    function autoPopulateIcons() {
      saveActivePixels();
      if (mode !== "dashboard") {
        setMode("dashboard");
      }

      const currentIcon = shuffled(DATA.currentIcons)[0];
      const forecastPool = DATA.forecastIcons.filter((icon) => icon.key !== currentIcon.key);
      const forecastIcons = shuffled(
        forecastPool.length >= FORECAST_ICON_BOXES.length ? forecastPool : DATA.forecastIcons
      ).slice(0, FORECAST_ICON_BOXES.length);
      const currentPosition = NIGHT_ICON_KEYS.has(currentIcon.key)
        ? CURRENT_ICON_NIGHT_POSITION
        : CURRENT_ICON_DAY_POSITION;

      fillPixels(
        CURRENT_ICON_CLEAR.x,
        CURRENT_ICON_CLEAR.y,
        CURRENT_ICON_CLEAR.width,
        CURRENT_ICON_CLEAR.height,
        BACKGROUND
      );
      pasteIcon(currentIcon, currentPosition.x, currentPosition.y);

      FORECAST_ICON_BOXES.forEach((box, index) => {
        fillPixels(box.x, box.y, box.width, box.height, BACKGROUND);
        pasteIcon(forecastIcons[index], box.x, box.y);
      });

      saveActivePixels();
      drawPixels();
      readout.textContent = `auto-populated icons: current ${currentIcon.codes}; forecast ${forecastIcons.map((icon) => icon.codes).join(", ")}`;
    }

    function makePalette() {
      for (const item of DATA.palette) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "swatch";
        button.title = item.name;
        button.style.background = item.color;
        button.addEventListener("click", () => {
          activeColor = item.color;
          document.querySelectorAll(".swatch").forEach((swatch) => swatch.classList.remove("active"));
          button.classList.add("active");
          readout.textContent = `active color ${item.name} ${item.color}`;
        });
        palette.appendChild(button);
      }
      palette.firstElementChild.classList.add("active");
    }

    function downloadPng() {
      const item = activeItem();
      const link = document.createElement("a");
      const name = item ? item.id.replace(/[^a-z0-9_-]+/gi, "-") : mode;
      link.download = `${mode}-${name}.png`;
      link.href = canvas.toDataURL("image/png");
      link.click();
    }

    async function copyJson() {
      const item = activeItem();
      const payload = {
        mode,
        id: item ? item.id : "",
        key: item && item.key ? item.key : "",
        width: activeWidth,
        height: activeHeight,
        pixels: activePixels
      };
      const text = JSON.stringify(payload, null, 2);
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        const textarea = document.createElement("textarea");
        textarea.value = text;
        textarea.style.position = "fixed";
        textarea.style.left = "-9999px";
        document.body.appendChild(textarea);
        textarea.focus();
        textarea.select();
        document.execCommand("copy");
        textarea.remove();
      }
      readout.textContent = "copied edited pixel JSON";
    }

    for (const [key, button] of Object.entries(modeButtons)) {
      button.addEventListener("click", () => setMode(key));
    }

    dashboardSelect.addEventListener("change", () => {
      saveActivePixels();
      loadItem(activeItem());
    });
    iconSelect.addEventListener("change", () => {
      saveActivePixels();
      loadItem(activeItem());
    });

    canvas.addEventListener("pointerdown", (event) => {
      painting = true;
      canvas.setPointerCapture(event.pointerId);
      paintAt(event);
    });
    canvas.addEventListener("pointermove", (event) => {
      if (painting) paintAt(event);
    });
    canvas.addEventListener("pointerup", () => {
      painting = false;
    });
    canvas.addEventListener("pointercancel", () => {
      painting = false;
    });

    document.getElementById("resetButton").addEventListener("click", () => {
      activePixels = clonePixels(originalPixels);
      saveActivePixels();
      drawPixels();
      readout.textContent = "selection reset";
    });
    document.getElementById("downloadButton").addEventListener("click", downloadPng);
    document.getElementById("copyButton").addEventListener("click", copyJson);
    document.getElementById("autoIconsButton").addEventListener("click", autoPopulateIcons);

    setOptions(dashboardSelect, DATA.dashboardCases);
    makePalette();
    setMode("dashboard");
  </script>
</body>
</html>
"""

    EDITOR_HTML.write_text(
        html.replace("__EDITOR_DATA__", json.dumps(data, separators=(",", ":"))),
        encoding="utf-8",
    )


def main():
    MOCKUP_DIR.mkdir(exist_ok=True)
    cases = [
        ("69 degrees", "dashboard-current.png", 68.8),
        ("101 degrees", "dashboard-current-101.png", 101),
        ("122 degrees", "dashboard-current-122.png", 122),
        ("negative", "dashboard-current-negative.png", -8),
    ]

    for label, filename, temperature in cases:
        image = render_dashboard(
            sample_weather(current_temp=temperature),
            blink=False,
            now=datetime(2026, 5, 29, 23, 7),
        )
        image.save(MOCKUP_DIR / filename)

    write_editor([(label, filename) for label, filename, temperature in cases])
    print(MOCKUP_IMAGE)


if __name__ == "__main__":
    main()
