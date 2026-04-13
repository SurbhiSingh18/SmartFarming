import requests
import random
import time
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("THINGSPEAK_KEY")

while True:
    moisture = random.randint(20, 80)
    temp = random.randint(20, 40)

    url = f"https://api.thingspeak.com/update?api_key={API_KEY}&field1={moisture}&field2={temp}"
    
    requests.get(url)

    print("Sent:", moisture, temp)
    time.sleep(10)