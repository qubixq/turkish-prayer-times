#!/usr/bin/env python3

import requests
import json
import os
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Tuple

# Turkish cities mapping (ID: Name)
TURKISH_CITIES = {
    1: "adana", 2: "adiyaman", 3: "afyonkarahisar", 4: "agri", 5: "amasya",
    6: "ankara", 7: "antalya", 8: "artvin", 9: "aydin", 10: "balikesir",
    11: "bilecik", 12: "bingol", 13: "bitlis", 14: "bolu", 15: "burdur",
    16: "bursa", 17: "canakkale", 18: "cankiri", 19: "corum", 20: "denizli",
    21: "diyarbakir", 22: "edirne", 23: "elazig", 24: "erzincan", 25: "erzurum",
    26: "eskisehir", 27: "gaziantep", 28: "giresun", 29: "gumushane", 30: "hakkari",
    31: "hatay", 32: "isparta", 33: "mersin", 34: "istanbul", 35: "izmir",
    36: "kars", 37: "kastamonu", 38: "kayseri", 39: "kirklareli", 40: "kirsehir",
    41: "kocaeli", 42: "konya", 43: "kutahya", 44: "malatya", 45: "manisa",
    46: "kahramanmaras", 47: "mardin", 48: "mugla", 49: "mus", 50: "nevsehir",
    51: "nigde", 52: "ordu", 53: "rize", 54: "sakarya", 55: "samsun",
    56: "siirt", 57: "sinop", 58: "sivas", 59: "tekirdag", 60: "tokat",
    61: "trabzon", 62: "tunceli", 63: "sanliurfa", 64: "usak", 65: "van",
    66: "yozgat", 67: "zonguldak", 68: "aksaray", 69: "bayburt", 70: "karaman",
    71: "kirikkale", 72: "batman", 73: "sirnak", 74: "bartin", 75: "ardahan",
    76: "igdir", 77: "yalova", 78: "karabuk", 79: "kilis", 80: "osmaniye",
    81: "duzce"
}

PRAYER_NAMES = ["İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı"]

def get_prayer_times(city_id: int) -> Dict:
    """Fetch prayer times from Diyanet API"""
    url = f"https://ezanvakti.herokuapp.com/vakitler/{city_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data for city {city_id}: {e}")
        return {}

def parse_time(time_str: str) -> datetime:
    """Parse time string to datetime object"""
    turkey_tz = pytz.timezone('Europe/Istanbul')
    today = datetime.now(turkey_tz).date()
    time_obj = datetime.strptime(time_str, "%H:%M").time()
    return turkey_tz.localize(datetime.combine(today, time_obj))

def get_current_prayer_info(prayer_times: List[str]) -> Tuple[str, int, int]:
    """Determine current prayer period and calculate elapsed/remaining time"""
    turkey_tz = pytz.timezone('Europe/Istanbul')
    now = datetime.now(turkey_tz)
    
    parsed_times = [parse_time(time) for time in prayer_times]
    
    # Find current prayer period
    current_prayer = "Yatsı"
    current_index = 5
    elapsed_minutes = 0
    remaining_minutes = 0
    
    for i, prayer_time in enumerate(parsed_times):
        if now >= prayer_time:
            current_prayer = PRAYER_NAMES[i]
            current_index = i
        else:
            break
    
    # Calculate elapsed time since current prayer
    current_prayer_time = parsed_times[current_index]
    elapsed = now - current_prayer_time
    elapsed_minutes = int(elapsed.total_seconds() / 60)
    
    # Calculate remaining time to next prayer
    if current_index < 5:
        next_prayer_time = parsed_times[current_index + 1]
        remaining = next_prayer_time - now
        remaining_minutes = int(remaining.total_seconds() / 60)
    else:
        # Next prayer is İmsak of next day
        tomorrow_imsak = parsed_times[0] + timedelta(days=1)
        remaining = tomorrow_imsak - now
        remaining_minutes = int(remaining.total_seconds() / 60)
    
    return current_prayer, elapsed_minutes, remaining_minutes

def format_output(city_name: str, prayer_data: Dict) -> str:
    """Format prayer times as terminal-friendly output"""
    if not prayer_data:
        return f"Error: Unable to fetch prayer times for {city_name.title()}"
    
    turkey_tz = pytz.timezone('Europe/Istanbul')
    current_time = datetime.now(turkey_tz)
    
    # Extract prayer times
    times = [
        prayer_data.get('imsak', '00:00'),
        prayer_data.get('gunes', '00:00'),
        prayer_data.get('ogle', '00:00'),
        prayer_data.get('ikindi', '00:00'),
        prayer_data.get('aksam', '00:00'),
        prayer_data.get('yatsi', '00:00')
    ]
    
    current_prayer, elapsed, remaining = get_current_prayer_info(times)
    
    # Build output
    output = []
    output.append(f"┌─────────────────────────────────────┐")
    output.append(f"│ {city_name.upper().center(35)} │")
    output.append(f"├─────────────────────────────────────┤")
    output.append(f"│ {current_time.strftime('%d.%m.%Y %H:%M').center(35)} │")
    output.append(f"├─────────────────────────────────────┤")
    
    for i, (prayer, time) in enumerate(zip(PRAYER_NAMES, times)):
        marker = "►" if prayer == current_prayer else " "
        output.append(f"│ {marker} {prayer:<8} {time:>8}           │")
    
    output.append(f"├─────────────────────────────────────┤")
    output.append(f"│ {current_prayer}: {elapsed}dk geçti, {remaining}dk kaldı │")
    output.append(f"└─────────────────────────────────────┘")
    
    return "\n".join(output)

def generate_city_file(city_id: int, city_name: str):
    """Generate prayer times file for a city"""
    print(f"Processing {city_name.title()}...")
    prayer_data = get_prayer_times(city_id)
    
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
    
    for city_id, city_name in TURKISH_CITIES.items():
        generate_city_file(city_id, city_name)
    
    print("\nAll files generated successfully!")

if __name__ == "__main__":
    main()
