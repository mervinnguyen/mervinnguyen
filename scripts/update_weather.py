import requests
from datetime import datetime, timezone

LAT = 33.7175
LON = -117.8311

# Fetch weather
weather = requests.get(
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    f"&current=temperature_2m,weathercode"
    f"&temperature_unit=fahrenheit"
).json()

# Fetch sunrise/sunset
sun = requests.get(
    f"https://api.sunrise-sunset.org/json?lat={LAT}&lng={LON}&formatted=0"
).json()

# Parse weather
temp = round(weather["current"]["temperature_2m"])
code = weather["current"]["weathercode"]

def get_condition(code):
    if code == 0: return "Clear sky"
    if code <= 3: return "Partly cloudy"
    if code <= 48: return "Foggy"
    if code <= 67: return "Rainy"
    if code <= 77: return "Snowy"
    if code <= 82: return "Showers"
    return "Stormy"

condition = get_condition(code)

# Parse sunrise/sunset to local time (PST/PDT)
def utc_to_local(utc_str):
    dt = datetime.fromisoformat(utc_str)
    # Convert to US/Pacific manually via offset
    local = dt.astimezone()
    return local.strftime("%H:%M")

sunrise = utc_to_local(sun["results"]["sunrise"])
sunset = utc_to_local(sun["results"]["sunset"])

# New weather line
new_line = (
    f"<br/>Currently, the weather is: <b>{temp}°F, <i>{condition}</i></b>"
    f"</br>Today, the sun rose at <b>{sunrise}</b> and sets at <b>{sunset}</b>.</p>"
)

# Replace in README
with open("README.md", "r") as f:
    content = f.read()

import re
updated = re.sub(
    r"<br/>Currently, the weather is:.*?</p>",
    new_line,
    content,
    flags=re.DOTALL
)

with open("README.md", "w") as f:
    f.write(updated)

print(f"Updated: {new_line}")
```