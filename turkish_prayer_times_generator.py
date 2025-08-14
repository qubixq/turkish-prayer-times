#!/usr/bin/env python3
# turkish_prayer_times_generator.py - Main script for generating prayer times

import requests
import json
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Tuple

# Turkish cities with their coordinates (latitude, longitude)
TURKISH_CITIES = {
    "adana": (37.0000, 35.3213),
    "adiyaman": (37.7648, 38.2786),
    "afyonkarahisar": (38.7507, 30.5567),
    "agri": (39.7191, 43.0503),
    "amasya": (40.6499, 35.8353),
    "ankara": (39.9334, 32.8597),
    "antalya": (36.8969, 30.7133),
    "artvin": (41.1828, 41.8183),
    "aydin": (37.8560, 27.8416),
    "balikesir": (39.6484, 27.8826),
    "bilecik": (40.1553, 29.9833),
    "bingol": (38.8846, 40.4939),
    "bitlis": (42.1069, 42.1133),
    "bolu": (40.7360, 31.6061),
    "burdur": (37.7268, 30.2900),
    "bursa": (40.1885, 29.0610),
    "canakkale": (40.1553, 26.4142),
    "cankiri": (40.6013, 33.6134),
    "corum": (40.5506, 34.9556),
    "denizli": (37.7765, 29.0864),
    "diyarbakir": (37.9144, 40.2306),
    "edirne": (41.6771, 26.5557),
    "elazig": (38.6810, 39.2264),
    "erzincan": (39.7500, 39.5000),
    "erzurum": (39.9000, 41.2700),
    "eskisehir": (39.7767, 30.5206),
    "gaziantep": (37.0594, 37.3825),
    "giresun": (40.9128, 38.3895),
    "gumushane": (40.4386, 39.5086),
    "hakkari": (37.5744, 43.7408),
    "hatay": (36.4018, 36.3498),
    "isparta": (37.7648, 30.5566),
    "mersin": (36.8000, 34.6333),
    "istanbul": (41.0082, 28.9784),
    "izmir": (38.4237, 27.1428),
    "kars": (40.6013, 43.0975),
    "kastamonu": (41.3887, 33.7827),
    "kayseri": (38.7312, 35.4787),
    "kirklareli": (41.7333, 27.2167),
    "kirsehir": (39.1425, 34.1709),
    "kocaeli": (40.8533, 29.8815),
    "konya": (37.8667, 32.4833),
    "kutahya": (39.4242, 29.9833),
    "malatya": (38.3552, 38.3095),
    "manisa": (38.6191, 27.4289),
    "kahramanmaras": (37.5858, 36.9371),
    "mardin": (37.3212, 40.7245),
    "mugla": (37.2153, 28.3636),
    "mus": (38.9462, 41.7539),
    "nevsehir": (38.6939, 34.6857),
    "nigde": (37.9667, 34.6833),
    "ordu": (40.9839, 37.8764),
    "rize": (41.0201, 40.5234),
    "sakarya": (40.6940, 30.4358),
    "samsun": (41.2867, 36.3300),
    "siirt": (37.9333, 41.9500),
    "sinop": (42.0231, 35.1531),
    "sivas": (39.7477, 37.0179),
    "tekirdag": (40.9833, 27.5167),
    "tokat": (40.3167, 36.5500),
    "trabzon": (41.0015, 39.7178),
    "tunceli": (39.3074, 39.4388),
    "sanliurfa": (37.1591, 38.7969),
    "usak": (38.6823, 29.4082),
    "van": (38.4891, 43.4089),
    "yozgat": (39.8181, 34.8147),
    "zonguldak": (41.4564, 31.7987),
    "aksaray": (38.3687, 34.0370),
    "bayburt": (40.2587, 40.2249),
    "karaman": (37.1759, 33.2287),
    "kirikkale": (39.8468, 33.5153),
    "batman": (37.8812, 41.1351),
    "sirnak": (37.4187, 42.4918),
    "bartin": (41.5811, 32.4610),
    "ardahan": (41.1105, 42.7022),
    "igdir": (39.8880, 44.0448),
    "yalova": (40.6500, 29.2667),
    "karabuk": (41.2061, 32.6204),
    "kilis": (36.7184, 37.1212),
    "osmaniye": (37.2130, 36.1763),
    "duzce": (40.8438, 31.1565)
}

PRAYER_NAMES = ["İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı"]

def get_prayer_times(latitude: float, longitude: float) -> Dict:
    """Fetch prayer times from AlAdhan API using coordinates"""
    url = f"https://api.aladhan.com/v1/timings"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'method': 13,  # Turkey method
        'timezone': 'Europe/Istanbul'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('code') == 200 and 'data' in data:
            return data['data']['timings']
        else:
            print(f"API returned error: {data}")
            return {}
            
    except Exception as e:
        print(f"Error fetching data for coordinates ({latitude}, {longitude}): {e}")
        return {}

def format_output(city_name: str, prayer_data: Dict) -> str:
    """Format prayer times as terminal-friendly output - only prayer times"""
    if not prayer_data:
        return f"Error: Unable to fetch prayer times for {city_name.title()}"
    
    # Map AlAdhan API response to our prayer names
    times = [
        prayer_data.get('Imsak', '00:00'),
        prayer_data.get('Sunrise', '00:00'), 
        prayer_data.get('Dhuhr', '00:00'),
        prayer_data.get('Asr', '00:00'),
        prayer_data.get('Maghrib', '00:00'),
        prayer_data.get('Isha', '00:00')
    ]
    
    # Clean times (remove timezone info)
    times = [time.split(' ')[0] for time in times]
    
    # Build simple output - just prayer times
    output = []
    output.append("┌─────────────────────────────────────┐")
    output.append(f"│ {city_name.upper().center(35)} │")
    output.append("├─────────────────────────────────────┤")
    
    for i, (prayer, time) in enumerate(zip(PRAYER_NAMES, times)):
        output.append(f"│   {prayer:<8} {time:>8}           │")
    
    output.append("└─────────────────────────────────────┘")
    
    return "\n".join(output)

def generate_city_file(city_name: str, coordinates: Tuple[float, float]):
    """Generate prayer times file for a city"""
    print(f"Processing {city_name.title()}...")
    latitude, longitude = coordinates
    prayer_data = get_prayer_times(latitude, longitude)
    
    if prayer_data:
        content = format_output(city_name, prayer_data)
        with open(f"{city_name}.txt", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Generated {city_name}.txt")
    else:
        print(f"✗ Failed to generate {city_name}.txt")

def main():
    """Generate all city prayer time files"""
    print("Generating Turkish Prayer Times TUI files...")
    print(f"Total cities: {len(TURKISH_CITIES)}")
    print("Using AlAdhan API with Turkey Diyanet method...")
    print("Simple format - only prayer times...")
    
    for city_name, coordinates in TURKISH_CITIES.items():
        generate_city_file(city_name, coordinates)
    
    print("\nAll files generated successfully!")

if __name__ == "__main__":
    main()
