from colors import blue, light_blue, yellow, orange, black, white, cyan, moon_gold, moon_highlight, moon_shadow, gray_light, gray_shadow

# height: 6, width: 8
def cloud(x,y):
    return [
        ((x+2,y), blue),
        ((x+3,y), blue),
        ((x+1,y+1), blue),
        ((x+1,y+2), blue),
        ((x,y+3), blue),
        ((x,y+4), blue),
        ((x+1,y+5), blue),
        ((x+2,y+5), blue),
        ((x+3,y+5), blue),
        ((x+4,y+5), blue),
        ((x+5,y+5), blue),
        ((x+6,y+5), blue),
        ((x+4,y+1), blue),
        ((x+4,y+2), blue),
        ((x+5,y+1), blue),
        ((x+6,y+2), blue),
        ((x+7,y+3), blue),
        ((x+7,y+4), blue),

        ((x+2,y+1), light_blue),
        ((x+3,y+1), light_blue),
        ((x+2,y+2), light_blue),
        ((x+3,y+2), light_blue),
        ((x+1,y+3), light_blue),
        ((x+2,y+3), light_blue),
        ((x+3,y+3), light_blue),
        ((x+4,y+3), light_blue),
        ((x+5,y+3), light_blue),
        ((x+6,y+3), light_blue),
        ((x+1,y+4), light_blue),
        ((x+2,y+4), light_blue),
        ((x+3,y+4), light_blue),
        ((x+4,y+4), light_blue),
        ((x+5,y+4), light_blue),
        ((x+6,y+4), light_blue),
        ((x+5,y+2), light_blue),
    ]

def gray_cloud(x,y):
    return [
        ((x+2,y), gray_shadow),
        ((x+3,y), gray_shadow),
        ((x+1,y+1), gray_shadow),
        ((x+1,y+2), gray_shadow),
        ((x,y+3), gray_shadow),
        ((x,y+4), gray_shadow),
        ((x+1,y+5), gray_shadow),
        ((x+2,y+5), gray_shadow),
        ((x+3,y+5), gray_shadow),
        ((x+4,y+5), gray_shadow),
        ((x+5,y+5), gray_shadow),
        ((x+6,y+5), gray_shadow),
        ((x+4,y+1), gray_shadow),
        ((x+4,y+2), gray_shadow),
        ((x+5,y+1), gray_shadow),
        ((x+6,y+2), gray_shadow),
        ((x+7,y+3), gray_shadow),
        ((x+7,y+4), gray_shadow),

        ((x+2,y+1), gray_light),
        ((x+3,y+1), gray_light),
        ((x+2,y+2), gray_light),
        ((x+3,y+2), gray_light),
        ((x+1,y+3), gray_light),
        ((x+2,y+3), gray_light),
        ((x+3,y+3), gray_light),
        ((x+4,y+3), gray_light),
        ((x+5,y+3), gray_light),
        ((x+6,y+3), gray_light),
        ((x+1,y+4), gray_light),
        ((x+2,y+4), gray_light),
        ((x+3,y+4), gray_light),
        ((x+4,y+4), gray_light),
        ((x+5,y+4), gray_light),
        ((x+6,y+4), gray_light),
        ((x+5,y+2), gray_light),
    ]

def small_cloud(x,y):
    return [
        ((x+1,y), blue),
        ((x+2,y), blue),
        ((x,y+1), blue),
        ((x+3,y+1), blue),
        ((x,y+2), blue),
        ((x+1,y+3), blue),
        ((x+2,y+3), blue),
        ((x+3,y+3), blue),
        ((x+1,y+1), light_blue),
        ((x+2,y+1), light_blue),
        ((x+1,y+2), light_blue),
        ((x+2,y+2), light_blue),
        ((x+3,y+2), light_blue),
    ]

def clear_sun(x,y):
    return sun(x,y)

def night_stars(x,y):
    return [
        ((x+18,y+3), white),
        ((x+17,y+4), white),
        ((x+18,y+4), moon_highlight),
        ((x+19,y+4), white),
        ((x+18,y+5), white),
        ((x+15,y+3), white),
        ((x+21,y+7), white),
    ]

def clear_moon(x,y):
    return night_stars(x,y) + moon(x,y)

def mostly_sunny(x,y):
    return sun(x,y) + small_cloud(x+5,y+4)

def previous_mostly_clear_night(x,y):
    return moon(x,y) + cloud(x+12,y+13)

def previous_mostly_clear_night_offset_cloud(x,y):
    return cloud(x+12,y+13) + moon(x,y)

def mostly_clear_night(x,y):
    return night_stars(x,y) + cloud(x+6,y+12) + moon(x,y)

def partly_cloudy(x,y):
    return sun(x,y) + cloud(x+1,y+3)

def previous_partly_cloudy_night(x,y):
    return moon(x,y) + cloud(x+10,y+12)

def previous_partly_cloudy_night_offset_cloud(x,y):
    return moon(x,y) + cloud(x+10,y+12)

def partly_cloudy_night(x,y):
    return night_stars(x,y) + moon(x,y) + cloud(x+6,y+12)

def previous_overcast(x,y):
    return cloud(x,y+1) + [
        ((x+1,y+6), blue),
        ((x+2,y+6), blue),
        ((x+3,y+6), blue),
        ((x+4,y+6), blue),
        ((x+5,y+6), blue),
        ((x+6,y+6), blue),
    ]

def previous_overcast_double_border(x,y):
    return cloud(x,y) + [
        ((x+1,y+6), blue),
        ((x+2,y+6), blue),
        ((x+3,y+6), blue),
        ((x+4,y+6), blue),
        ((x+5,y+6), blue),
        ((x+6,y+6), blue),
    ]

def overcast(x,y):
    return cloud(x,y)

def previous_fog(x,y):
    return cloud(x,y) + [
        ((x,y+6), light_blue),
        ((x+1,y+6), light_blue),
        ((x+3,y+6), light_blue),
        ((x+4,y+6), light_blue),
        ((x+6,y+6), light_blue),
        ((x+7,y+6), light_blue),
        ((x+1,y+8), blue),
        ((x+2,y+8), blue),
        ((x+4,y+8), blue),
        ((x+5,y+8), blue),
    ]

def fog(x,y):
    return cloud(x,y) + [
        ((x+0,y+6), light_blue),
        ((x+1,y+6), light_blue),
        ((x+2,y+6), light_blue),
        ((x+5,y+6), light_blue),
        ((x+6,y+6), light_blue),
        ((x+7,y+6), light_blue),
        ((x+3,y+7), light_blue),
        ((x+4,y+7), light_blue),
        ((x+1,y+8), blue),
        ((x+2,y+8), blue),
        ((x+3,y+8), blue),
        ((x+5,y+8), blue),
        ((x+6,y+8), blue),
        ((x+7,y+8), blue),
    ]

def previous_rime_fog_original_icy(x,y):
    return previous_fog(x,y) + [
        ((x+0,y+7), cyan),
        ((x+3,y+7), white),
        ((x+6,y+7), cyan),
        ((x+7,y+8), white),
    ]

def previous_rime_fog(x,y):
    return fog(x,y)

def rime_fog(x,y):
    return [
        ((x+2,y+0), blue),
        ((x+3,y+0), blue),
        ((x+1,y+1), blue),
        ((x+2,y+1), light_blue),
        ((x+3,y+1), light_blue),
        ((x+4,y+1), blue),
        ((x+5,y+1), blue),
        ((x+1,y+2), blue),
        ((x+2,y+2), light_blue),
        ((x+3,y+2), light_blue),
        ((x+4,y+2), blue),
        ((x+5,y+2), light_blue),
        ((x+6,y+2), blue),
        ((x+0,y+3), blue),
        ((x+1,y+3), light_blue),
        ((x+2,y+3), light_blue),
        ((x+3,y+3), light_blue),
        ((x+4,y+3), light_blue),
        ((x+5,y+3), light_blue),
        ((x+6,y+3), light_blue),
        ((x+7,y+3), blue),
        ((x+0,y+4), blue),
        ((x+1,y+4), light_blue),
        ((x+2,y+4), light_blue),
        ((x+3,y+4), light_blue),
        ((x+4,y+4), light_blue),
        ((x+5,y+4), light_blue),
        ((x+6,y+4), light_blue),
        ((x+7,y+4), blue),
        ((x+1,y+5), blue),
        ((x+2,y+5), blue),
        ((x+3,y+5), blue),
        ((x+4,y+5), blue),
        ((x+5,y+5), blue),
        ((x+6,y+5), blue),
        ((x+0,y+6), light_blue),
        ((x+1,y+6), light_blue),
        ((x+2,y+6), light_blue),
        ((x+5,y+6), light_blue),
        ((x+6,y+6), light_blue),
        ((x+7,y+6), light_blue),
        ((x+3,y+7), light_blue),
        ((x+4,y+7), light_blue),
        ((x+1,y+8), white),
        ((x+2,y+8), white),
        ((x+3,y+8), white),
        ((x+5,y+8), white),
        ((x+6,y+8), white),
        ((x+7,y+8), white),
    ]

def drizzle(x,y):
    return cloud(x,y) + [
        ((x+2,y+6), light_blue),
        ((x+5,y+7), light_blue),
    ]

def freezing_drizzle(x,y):
    return cloud(x,y) + [
        ((x+2,y+6), cyan),
        ((x+5,y+7), cyan),
        ((x+3,y+8), white),
    ]

def rain(x,y):
    return cloud(x,y) + [
        ((x+1,y+6), light_blue),
        ((x+5,y+6), light_blue),
        ((x+3,y+7), light_blue),
        ((x+7,y+7), light_blue),
    ]

def previous_heavy_rain_dense_lines(x,y):
    return cloud(x,y) + [
        ((x+0,y+6), light_blue),
        ((x+0,y+7), blue),
        ((x+0,y+8), light_blue),
        ((x+2,y+6), light_blue),
        ((x+2,y+7), blue),
        ((x+2,y+8), light_blue),
        ((x+4,y+6), light_blue),
        ((x+4,y+7), blue),
        ((x+4,y+8), light_blue),
        ((x+6,y+6), light_blue),
        ((x+6,y+7), blue),
        ((x+6,y+8), light_blue),
        ((x+8,y+6), light_blue),
        ((x+8,y+7), blue),
        ((x+8,y+8), light_blue),
    ]

def previous_heavy_rain(x,y):
    return cloud(x,y) + [
        ((x+1,y+6), light_blue),
        ((x+5,y+6), light_blue),
        ((x+1,y+7), blue),
        ((x+3,y+7), light_blue),
        ((x+5,y+7), blue),
        ((x+7,y+7), light_blue),
        ((x+2,y+8), light_blue),
        ((x+4,y+8), blue),
        ((x+6,y+8), light_blue),
        ((x+8,y+8), blue),
    ]

def heavy_rain(x,y):
    return [
        ((x+2,y+0), blue),
        ((x+3,y+0), blue),
        ((x+1,y+1), blue),
        ((x+2,y+1), light_blue),
        ((x+3,y+1), light_blue),
        ((x+4,y+1), blue),
        ((x+5,y+1), blue),
        ((x+1,y+2), blue),
        ((x+2,y+2), light_blue),
        ((x+3,y+2), light_blue),
        ((x+4,y+2), blue),
        ((x+5,y+2), light_blue),
        ((x+6,y+2), blue),
        ((x+0,y+3), blue),
        ((x+1,y+3), light_blue),
        ((x+2,y+3), light_blue),
        ((x+3,y+3), light_blue),
        ((x+4,y+3), light_blue),
        ((x+5,y+3), light_blue),
        ((x+6,y+3), light_blue),
        ((x+7,y+3), blue),
        ((x+0,y+4), blue),
        ((x+1,y+4), light_blue),
        ((x+2,y+4), light_blue),
        ((x+3,y+4), light_blue),
        ((x+4,y+4), light_blue),
        ((x+5,y+4), light_blue),
        ((x+6,y+4), light_blue),
        ((x+7,y+4), blue),
        ((x+1,y+5), blue),
        ((x+2,y+5), blue),
        ((x+3,y+5), blue),
        ((x+4,y+5), blue),
        ((x+5,y+5), blue),
        ((x+6,y+5), blue),
        ((x+1,y+6), light_blue),
        ((x+5,y+6), light_blue),
        ((x+1,y+7), blue),
        ((x+3,y+7), light_blue),
        ((x+5,y+7), blue),
        ((x+7,y+7), light_blue),
        ((x+1,y+8), blue),
        ((x+3,y+8), blue),
        ((x+5,y+8), blue),
        ((x+7,y+8), blue),
        ((x+3,y+9), blue),
        ((x+7,y+9), blue),
    ]

def freezing_rain(x,y):
    return cloud(x,y) + [
        ((x+1,y+6), cyan),
        ((x+5,y+6), cyan),
        ((x+1,y+7), white),
        ((x+3,y+7), cyan),
        ((x+5,y+7), white),
        ((x+7,y+7), cyan),
        ((x+3,y+8), white),
        ((x+7,y+8), white),
    ]

def snow(x,y):
    return cloud(x,y) + [
        ((x+1,y+6), white),
        ((x+5,y+6), white),
        ((x+3,y+7), white),
        ((x+7,y+7), white),
    ]

def heavy_snow(x,y):
    return cloud(x,y) + [
        ((x+1,y+6), white),
        ((x+3,y+6), white),
        ((x+5,y+6), white),
        ((x+7,y+6), white),
        ((x+2,y+7), white),
        ((x+4,y+7), white),
        ((x+6,y+7), white),
        ((x+1,y+8), white),
        ((x+5,y+8), white),
    ]

def previous_heavy_snow_showers(x,y):
    return heavy_snow(x,y)

def heavy_snow_showers(x,y):
    return [
        ((x+2,y+0), blue),
        ((x+3,y+0), blue),
        ((x+1,y+1), blue),
        ((x+2,y+1), light_blue),
        ((x+3,y+1), light_blue),
        ((x+4,y+1), blue),
        ((x+5,y+1), blue),
        ((x+1,y+2), blue),
        ((x+2,y+2), light_blue),
        ((x+3,y+2), light_blue),
        ((x+4,y+2), blue),
        ((x+5,y+2), light_blue),
        ((x+6,y+2), blue),
        ((x+0,y+3), blue),
        ((x+1,y+3), light_blue),
        ((x+2,y+3), light_blue),
        ((x+3,y+3), light_blue),
        ((x+4,y+3), light_blue),
        ((x+5,y+3), light_blue),
        ((x+6,y+3), light_blue),
        ((x+7,y+3), blue),
        ((x+0,y+4), blue),
        ((x+1,y+4), light_blue),
        ((x+2,y+4), light_blue),
        ((x+3,y+4), light_blue),
        ((x+4,y+4), light_blue),
        ((x+5,y+4), light_blue),
        ((x+6,y+4), light_blue),
        ((x+7,y+4), blue),
        ((x+1,y+5), blue),
        ((x+2,y+5), blue),
        ((x+3,y+5), blue),
        ((x+4,y+5), blue),
        ((x+5,y+5), blue),
        ((x+6,y+5), blue),
        ((x+1,y+6), cyan),
        ((x+3,y+6), white),
        ((x+5,y+6), white),
        ((x+7,y+6), cyan),
        ((x+2,y+7), white),
        ((x+4,y+7), cyan),
        ((x+6,y+7), white),
        ((x+1,y+8), white),
        ((x+5,y+8), white),
    ]

def snow_grains(x,y):
    return cloud(x,y) + [
        ((x+1,y+6), white),
        ((x+3,y+6), white),
        ((x+6,y+6), cyan),
        ((x+2,y+8), cyan),
        ((x+5,y+8), white),
        ((x+7,y+8), white),
    ]

def previous_rain_showers(x,y):
    return cloud(x,y) + [
        ((x+0,y+7), light_blue),
        ((x+1,y+7), light_blue),
        ((x+4,y+6), blue),
        ((x+6,y+8), light_blue),
        ((x+7,y+8), light_blue),
        ((x+8,y+7), blue),
    ]

def rain_showers(x,y):
    return cloud(x,y) + [
        ((x+0,y+7), light_blue),
        ((x+3,y+6), light_blue),
        ((x+5,y+8), blue),
        ((x+8,y+7), light_blue),
    ]

def previous_violent_showers(x,y):
    return cloud(x,y) + [
        ((x+0,y+6), light_blue),
        ((x+2,y+6), blue),
        ((x+4,y+6), light_blue),
        ((x+6,y+6), blue),
        ((x+8,y+6), light_blue),
        ((x+1,y+7), blue),
        ((x+3,y+8), light_blue),
        ((x+5,y+7), blue),
        ((x+7,y+8), light_blue),
    ]

def violent_showers(x,y):
    return cloud(x,y) + [
        ((x+0,y+6), light_blue),
        ((x+2,y+7), blue),
        ((x+3,y+8), light_blue),
        ((x+5,y+6), light_blue),
        ((x+6,y+7), blue),
        ((x+8,y+8), light_blue),
        ((x+1,y+8), blue),
        ((x+7,y+6), light_blue),
    ]

def snow_showers(x,y):
    return cloud(x,y) + [
        ((x+0,y+7), white),
        ((x+2,y+6), cyan),
        ((x+4,y+8), white),
        ((x+6,y+6), white),
        ((x+8,y+7), cyan),
    ]

def thunderstorm(x,y):
    return cloud(x,y) + [
        ((x+4,y+6), yellow),
        ((x+3,y+7), yellow),
        ((x+4,y+7), yellow),
        ((x+3,y+8), orange),
    ]

def hailstorm(x,y):
    return thunderstorm(x,y) + [
        ((x+1,y+7), white),
        ((x+6,y+7), white),
        ((x+5,y+8), cyan),
    ]

def previous_fallback_cloud(x,y):
    return cloud(x,y+1)

def fallback_cloud(x,y):
    return cloud(x,y)

def previous_weather_unknown(x,y):
    return gray_cloud(x,y+1) + [
        ((x+4,y+2), orange),
        ((x+5,y+2), orange),
        ((x+5,y+3), orange),
        ((x+4,y+4), orange),
        ((x+4,y+6), yellow),
    ]

def previous_weather_unknown_lower_yellow(x,y):
    return gray_cloud(x,y) + [
        ((x+4,y+5), yellow),
        ((x+5,y+5), yellow),
        ((x+5,y+6), yellow),
        ((x+4,y+7), yellow),
        ((x+4,y+9), yellow),
    ]

def weather_unknown(x,y):
    return gray_cloud(x,y) + [
        ((x+4,y+5), orange),
        ((x+5,y+5), orange),
        ((x+5,y+6), orange),
        ((x+4,y+7), orange),
        ((x+4,y+9), orange),
    ]

rainy = rain
dizzle = drizzle
thunder = thunderstorm
thunder_hail = hailstorm

# height: 8, width: 8
def sun(x,y):
    return [
        ((x+3,y), yellow),
        ((x+4,y), yellow),
        ((x+1,y+1), yellow),
        ((x,y+3), yellow),
        ((x,y+4), yellow),
        ((x+1,y+6), yellow),
        ((x+3,y+7), yellow),
        ((x+4,y+7), yellow),
        ((x+4,y+7), yellow),
        ((x+6,y+1), yellow),
        ((x+7,y+3), yellow),
        ((x+7,y+4), yellow),
        ((x+6,y+6), yellow),
        ((x+3,y+2), yellow),
        ((x+4,y+2), yellow),
        ((x+2,y+3), yellow),
        ((x+3,y+3), yellow),
        ((x+4,y+3), yellow),
        ((x+5,y+3), yellow),
        ((x+2,y+4), yellow),
        ((x+3,y+4), yellow),
        ((x+4,y+4), yellow),
        ((x+5,y+4), orange),
        ((x+3,y+5), orange),
        ((x+4,y+5), orange),
    ]

def previous_moon(x,y):
    pixels = []
    outer_center = (12.0, 12.0)
    cutout_center = (15.8, 9.5)
    radius_squared = 10.5 * 10.5

    for py in range(24):
        for px in range(24):
            center_x = px + 0.5
            center_y = py + 0.5
            outer_distance_squared = (
                (center_x - outer_center[0]) ** 2
                + (center_y - outer_center[1]) ** 2
            )
            cutout_distance_squared = (
                (center_x - cutout_center[0]) ** 2
                + (center_y - cutout_center[1]) ** 2
            )

            if outer_distance_squared <= radius_squared and cutout_distance_squared > radius_squared:
                if py <= 5 or px <= 4:
                    color = moon_highlight
                elif py >= 18 or px >= 16:
                    color = moon_shadow
                else:
                    color = moon_gold
                pixels.append(((x + px, y + py), color))
    return pixels

def previous_moon_before_lower_right_shave(x,y):
    pixels = []
    outer_center = (12.0, 12.0)
    cutout_center = (17.2, 10.2)
    radius_squared = 10.5 * 10.5

    for py in range(24):
        for px in range(24):
            center_x = px + 0.5
            center_y = py + 0.5
            outer_distance_squared = (
                (center_x - outer_center[0]) ** 2
                + (center_y - outer_center[1]) ** 2
            )
            cutout_distance_squared = (
                (center_x - cutout_center[0]) ** 2
                + (center_y - cutout_center[1]) ** 2
            )

            if outer_distance_squared <= radius_squared and cutout_distance_squared > radius_squared:
                if py <= 5 or px <= 4:
                    color = moon_highlight
                elif py >= 18 or px >= 16:
                    color = moon_shadow
                else:
                    color = moon_gold
                pixels.append(((x + px, y + py), color))
    return pixels

def moon(x,y):
    return previous_moon_before_lower_right_shave(x,y)


def pixel_art(x, y, rows, palette):
    pixels = []
    for row_index, row in enumerate(rows):
        for column_index, key in enumerate(row):
            color = palette.get(key)
            if color:
                pixels.append(((x + column_index, y + row_index), color))
    return pixels

def lineX(x_start,length,y):
    i = x_start
    result = []
    while i < length:
        result = result + [(i,y)]
        i += 1
    return result

def lineY(y_start,length,x):
    i = 0
    result = []
    while i < length:
        result = result + [(x,y_start)]
        y_start += 1
        i += 1
    return result

# 19
def bigSun(x,y):
    return [
        ((x+9,y), yellow),
        ((x+9,y+1), yellow),

        ((x+9,y+17), orange),
        ((x+9,y+18), orange),

        ((x,y+9), yellow),
        ((x+1,y+9), yellow),
        
        ((x+17,y+9), orange),
        ((x+18,y+9), orange),

        ((x+1,y+1), yellow),
        ((x+2,y+2), yellow),
        ((x+3,y+3), yellow),

        ((x+17,y+1), yellow),
        ((x+16,y+2), yellow),
        ((x+15,y+3), yellow),

        ((x+17,y+17), orange),
        ((x+16,y+16), orange),
        ((x+15,y+15), orange),

        ((x+1,y+17), yellow),
        ((x+2,y+16), yellow),
        ((x+3,y+15), yellow),

        ((x+7,y+3), yellow),
        ((x+8,y+3), yellow),
        ((x+9,y+3), yellow),
        ((x+10,y+3), yellow),
        ((x+11,y+3), yellow),

        ((x+5,y+4), yellow),
        ((x+6,y+4), yellow),
        ((x+7,y+4), yellow),
        ((x+8,y+4), yellow),
        ((x+9,y+4), yellow),
        ((x+10,y+4), yellow),
        ((x+11,y+4), yellow),
        ((x+12,y+4), yellow),
        ((x+13,y+4), yellow),

        ((x+4,y+5), yellow),
        ((x+5,y+5), yellow),
        ((x+6,y+5), black),
        ((x+7,y+5), yellow),
        ((x+8,y+5), yellow),
        ((x+9,y+5), yellow),
        ((x+10,y+5), yellow),
        ((x+11,y+5), black),
        ((x+12,y+5), yellow),
        ((x+13,y+5), yellow),
        ((x+14,y+5), orange),

        ((x+4,y+6), yellow),
        ((x+5,y+6), yellow),
        ((x+6,y+6), black),
        ((x+7,y+6), yellow),
        ((x+8,y+6), yellow),
        ((x+9,y+6), yellow),
        ((x+10,y+6), yellow),
        ((x+11,y+6), black),
        ((x+12,y+6), yellow),
        ((x+13,y+6), yellow),
        ((x+14,y+6), orange),

        ((x+3,y+7), yellow),
        ((x+4,y+7), yellow),
        ((x+5,y+7), yellow),
        ((x+6,y+7), black),
        ((x+7,y+7), yellow),
        ((x+8,y+7), yellow),
        ((x+9,y+7), yellow),
        ((x+10,y+7), yellow),
        ((x+11,y+7), black),
        ((x+12,y+7), yellow),
        ((x+13,y+7), yellow),
        ((x+14,y+7), yellow),
        ((x+15,y+7), orange),

        ((x+3,y+8), yellow),
        ((x+4,y+8), yellow),
        ((x+5,y+8), yellow),
        ((x+6,y+8), black),
        ((x+7,y+8), yellow),
        ((x+8,y+8), yellow),
        ((x+9,y+8), yellow),
        ((x+10,y+8), yellow),
        ((x+11,y+8), black),
        ((x+12,y+8), yellow),
        ((x+13,y+8), yellow),
        ((x+14,y+8), yellow),
        ((x+15,y+8), orange),

        ((x+3,y+9), yellow),
        ((x+4,y+9), yellow),
        ((x+5,y+9), yellow),
        ((x+6,y+9), yellow),
        ((x+7,y+9), yellow),
        ((x+8,y+9), yellow),
        ((x+9,y+9), yellow),
        ((x+10,y+9), yellow),
        ((x+11,y+9), yellow),
        ((x+12,y+9), yellow),
        ((x+13,y+9), yellow),
        ((x+14,y+9), yellow),
        ((x+15,y+9), orange),

        ((x+3,y+10), yellow),
        ((x+4,y+10), yellow),
        ((x+5,y+10), yellow),
        ((x+6,y+10), yellow),
        ((x+7,y+10), yellow),
        ((x+8,y+10), yellow),
        ((x+9,y+10), yellow),
        ((x+10,y+10), yellow),
        ((x+11,y+10), yellow),
        ((x+12,y+10), yellow),
        ((x+13,y+10), yellow),
        ((x+14,y+10), yellow),
        ((x+15,y+10), orange),

        ((x+3,y+11), yellow),
        ((x+4,y+11), yellow),
        ((x+5,y+11), yellow),
        ((x+6,y+11), yellow),
        ((x+7,y+11), yellow),
        ((x+8,y+11), yellow),
        ((x+9,y+11), yellow),
        ((x+10,y+11), yellow),
        ((x+11,y+11), yellow),
        ((x+12,y+11), yellow),
        ((x+13,y+11), yellow),
        ((x+14,y+11), yellow),
        ((x+15,y+11), orange),

        ((x+4,y+12), yellow),
        ((x+5,y+12), yellow),
        ((x+6,y+12), black),
        ((x+7,y+12), yellow),
        ((x+8,y+12), yellow),
        ((x+9,y+12), yellow),
        ((x+10,y+12), yellow),
        ((x+11,y+12), black),
        ((x+12,y+12), yellow),
        ((x+13,y+12), yellow),
        ((x+14,y+12), orange),

        ((x+4,y+13), yellow),
        ((x+5,y+13), yellow),
        ((x+6,y+13), yellow),
        ((x+7,y+13), black),
        ((x+8,y+13), black),
        ((x+9,y+13), black),
        ((x+10,y+13), black),
        ((x+11,y+13), yellow),
        ((x+12,y+13), yellow),
        ((x+13,y+13), yellow),
        ((x+14,y+13), orange),

        ((x+5,y+14), yellow),
        ((x+6,y+14), yellow),
        ((x+7,y+14), yellow),
        ((x+8,y+14), yellow),
        ((x+9,y+14), yellow),
        ((x+10,y+14), yellow),
        ((x+11,y+14), yellow),
        ((x+12,y+14), yellow),
        ((x+13,y+14), orange),

        ((x+7,y+15), orange),
        ((x+8,y+15), orange),
        ((x+9,y+15), orange),
        ((x+10,y+15), orange),
        ((x+11,y+15), orange),
    ]
