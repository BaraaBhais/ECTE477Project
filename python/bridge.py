import requests
import time
import random

API_KEY = "4I4E3QPZUH66N3JL"
URL = "https://api.thingspeak.com/update"

TEMP_ALERT_THRESHOLD = 30
GAS_ALERT_THRESHOLD = 400
DARK_LIGHT_THRESHOLD = 200
NO_MOTION_OFF_SECONDS = 30

last_motion_time = time.time()
light_status = 0

while True:
    temperature = random.randint(20, 40)
    humidity = random.randint(40, 90)
    light_level = random.randint(0, 500)
    motion = random.randint(0, 1)
    gas_level = random.randint(200, 600)

    # Demo mode: make light_status change often
    light_status = motion

    if temperature > TEMP_ALERT_THRESHOLD:
        print("FAN ON ALERT: Temperature =", temperature)

    if gas_level > GAS_ALERT_THRESHOLD:
        print("FIRE/GAS EMERGENCY ALERT: Gas =", gas_level)

    # Optional logic (kept, but light_status already follows motion for demo)
    if motion == 1:
        last_motion_time = time.time()
        if light_level < DARK_LIGHT_THRESHOLD:
            light_status = 1

    if (time.time() - last_motion_time) >= NO_MOTION_OFF_SECONDS:
        light_status = 0

    data = {
        "api_key": API_KEY,
        "field1": temperature,
        "field2": humidity,
        "field3": light_level,
        "field4": motion,
        "field5": gas_level,
        "field6": light_status
    }

    try:
        r = requests.get(URL, params=data, timeout=10)
        print("Sent:", data, "| status:", r.status_code, "| response:", r.text)
    except Exception as e:
        print("ERROR sending to ThingSpeak:", e)

    time.sleep(20)
