import requests
import time
import random

API_KEY = "PASTE_YOUR_THINGSPEAK_WRITE_KEY"

URL = "https://api.thingspeak.com/update"

while True:

    temperature = random.randint(20, 40)
    humidity = random.randint(40, 90)
    light = random.randint(0, 500)
    motion = random.randint(0, 1)
    gas = random.randint(200, 600)

    if motion == 1 and light < 200:
        light_status = 1
    else:
        light_status = 0

    data = {
        "api_key": API_KEY,
        "field1": temperature,
        "field2": humidity,
        "field3": light,
        "field4": motion,
        "field5": gas,
        "field6": light_status
    }

    response = requests.get(URL, params=data)

    print("Data sent:", data)

    time.sleep(15)