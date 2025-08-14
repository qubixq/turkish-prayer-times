import requests
from datetime import datetime
import pytz
from pathlib import Path

CITIES = [
    "adana","adiyaman","afyonkarahisar","agri","amasya","ankara","antalya",
    "artvin","aydin","balikesir","bilecik","bingol","bitlis","bolu","burdur",
    "bursa","canakkale","cankiri","corum","denizli","diyarbakir","edirne",
    "elazig","erzincan","erzurum","eskisehir","gaziantep","giresun","gumushane",
    "hakkari","hatay","isparta","mersin","istanbul","izmir","kars","kastamonu",
    "kayseri","kirklareli","kirsehir","kocaeli","konya","kutahya","malatya",
    "manisa","kahramanmaras","mardin","mugla","mus","nevsehir","nigde","ordu",
    "rize","sakarya","samsun","siirt","sinop","sivas","tekirdag","tokat",
    "trabzon","tunceli","sanliurfa","usak","van","yozgat","zonguldak",
    "aksaray","bayburt","karaman","kirikkale","batman","sirnak","bartin",
    "ardahan","igdir","yalova","karabuk","kilis","osmaniye","duzce"
]

def fetch_times(city):
    r = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Turkey&method=13")
    t = r.json()["data"]["timings"]
    return {
        "imsak": t["Fajr"], "gunes": t["Sunrise"], "ogle": t["Dhuhr"],
        "ikindi": t["Asr"], "aksam": t["Maghrib"], "yatsi": t["Isha"]
    }

def diff_str(a, b):
    m = int((b-a).total_seconds()//60)
    return f"{abs(m)//60:02}:{abs(m)%60:02}"

def generate(city):
    tz = pytz.timezone("Europe/Istanbul")
    now = datetime.now(tz)
    times = fetch_times(city)
    dt = {k: tz.localize(datetime(now.year, now.month, now.day, *map(int, v.split(":")))) for k, v in times.items()}
    keys = ["imsak","gunes","ogle","ikindi","aksam","yatsi"]
    current = None
    nextp = None
    for k in keys:
        if now < dt[k]:
            nextp = k
            break
        current = k
    lines = []
    lines.append(f"┌────── {city.capitalize()} ──────┐")
    lines.append(f"│ {now.strftime('%d %B %Y %H:%M'):<26}│")
    lines.append("├───────────────────────────────┤")
    for k, label in [("imsak","İmsak"),("gunes","Güneş"),("ogle","Öğle"),
                     ("ikindi","İkindi"),("aksam","Akşam"),("yatsi","Yatsı")]:
        lines.append(f"│ {label:<7} │ {times[k]:<15}│")
    lines.append("├───────────────────────────────┤")
    if current and nextp:
        lines.append(f"│ Now: {current.capitalize():<20}│")
        lines.append(f"│ Since {current}: {diff_str(dt[current], now):<11}│")
        lines.append(f"│ To {nextp}: {diff_str(now, dt[nextp]):<14}│")
    lines.append("└───────────────────────────────┘")
    return "\n".join(lines)

if __name__ == "__main__":
    out = Path(__file__).parent.parent
    for city in CITIES:
        (out / city).write_text(generate(city), encoding="utf-8")
