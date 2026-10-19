# Dashboard Editor

The dashboard editor is a local browser tool for inspecting and editing the
64x64 Pixoo dashboard grid and weather icon pixels.

It is intentionally simple: it shows the actual 64x64 pixel output enlarged with
nearest-neighbor scaling so layout decisions match the Pixoo display.

## Generate The Editor

Run:

```bash
python make_dashboard_mockup.py
```

Open:

```text
mockups/dashboard-editor.html
```

The generated HTML file is static. It does not need a web server.

## What It Shows

The editor contains:

- one enlarged 64x64 dashboard preview
- x/y grid labels for pixel-coordinate inspection
- direct pixel painting inside the enlarged grid
- a small project color palette
- current-condition icon editing
- forecast icon editing
- per-icon selectors
- PNG export
- JSON export
- an auto-populate button for quickly filling dashboard icon slots with varied
  test icons

## Editor Modes

Dashboard mode edits the enlarged 64x64 dashboard mockup.

Current icon mode edits one selected current-condition icon at a time. These
icons use the current-weather icon area and are designed around a `24x24`
target.

Forecast icon mode edits one selected forecast icon at a time. Forecast icons
are smaller and should remain visually simple. The current renderer places
forecast icons inside a fixed `12x10` forecast icon box.

Switching icons keeps browser-session edits isolated to the selected item.
Editing one weather icon should not change any other icon.

## Pixel Painting

Choose a palette color, then click or drag in the enlarged grid.

The palette includes common project colors such as:

- off/transparent black
- snow white
- cloud blues/grays
- bluish rain/cyan
- warm sun/moon yellow
- orange/yellow accent colors

This is not meant to be a full image editor. It is a focused pixel-review tool
for Pixoo-sized graphics.

## Exports

Download PNG exports when you want a visual record of an edit.

Copy JSON exports when an icon edit should be applied back into source code.

Important: browser edits do not automatically rewrite Python icon functions.
The current icon source is still function-drawn pixel art in `functions.py` and
`icon_sets/legacy_functions.py`. Applying an editor export is a deliberate code
change.

## Preview Accuracy

The editor is intended to be pixel accurate for the generated dashboard mockup.
It should use nearest-neighbor scaling and avoid responsive browser layout that
changes the actual 64x64 pixel composition.

The physical Pixoo display can still look different because of brightness,
diffusion, viewing distance, and the Pixoo upload/render path. Check the result on the physical display.
