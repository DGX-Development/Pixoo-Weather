from typing import List


class WeatherResponse:
    def __init__(self, latitude: float, longitude: float, generationtime_ms: float, 
                 utc_offset_seconds: int, timezone: str, timezone_abbreviation: str, 
                 elevation: float, current_units: 'CurrentUnits', current: 'Current', 
                 daily_units: 'DailyUnits', daily: 'Daily'):
        self.latitude = latitude
        self.longitude = longitude
        self.generationtime_ms = generationtime_ms
        self.utc_offset_seconds = utc_offset_seconds
        self.timezone = timezone
        self.timezone_abbreviation = timezone_abbreviation
        self.elevation = elevation
        self.current_units = current_units
        self.current = current
        self.daily_units = daily_units
        self.daily = daily

class CurrentUnits:
    def __init__(self, time: str, interval: str, temperature_2m: str, weather_code: str, is_day: str = None):
        self.time = time
        self.interval = interval
        self.temperature_2m = temperature_2m
        self.weather_code = weather_code
        self.is_day = is_day

class Current:
    def __init__(self, time: str, interval: int, temperature_2m: float, weather_code: int, is_day: int = None):
        self.time = time
        self.interval = interval
        self.temperature_2m = temperature_2m
        self.weather_code = weather_code
        self.is_day = is_day

class DailyUnits:
    def __init__(self, time: str, weather_code: str, temperature_2m_max: str, temperature_2m_min: str):
        self.time = time
        self.weather_code = weather_code
        self.temperature_2m_max = temperature_2m_max
        self.temperature_2m_min = temperature_2m_min

class Daily:
    def __init__(self, time: List[str], weather_code: List[int], temperature_2m_max: List[float], temperature_2m_min: List[float]):
        self.time = time
        self.weather_code = weather_code
        self.temperature_2m_max = temperature_2m_max
        self.temperature_2m_min = temperature_2m_min

def weather_response_object_hook(dct):
    if 'latitude' in dct and 'longitude' in dct:
        return WeatherResponse(
            latitude=dct['latitude'],
            longitude=dct['longitude'],
            generationtime_ms=dct['generationtime_ms'],
            utc_offset_seconds=dct['utc_offset_seconds'],
            timezone=dct['timezone'],
            timezone_abbreviation=dct['timezone_abbreviation'],
            elevation=dct['elevation'],
            current_units=CurrentUnits(**dct['current_units']),
            current=Current(**dct['current']),
            daily_units=DailyUnits(**dct['daily_units']),
            daily=Daily(**dct['daily'])
        )
    return dct
