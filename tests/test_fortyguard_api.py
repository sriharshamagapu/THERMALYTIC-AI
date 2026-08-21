import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("FORTYGUARD_API_KEY")

if not API_KEY:
    raise RuntimeError("FORTYGUARD_API_KEY not found in .env")


url = "https://api.fortyguard.com/v1/system/fetch-api-key-usage"

headers = {
    "api-key": API_KEY,
    "Content-Type": "application/json",
}

payload = {
    "api_key": API_KEY,
    "request": {}
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=30,
)

print("HTTP status:", response.status_code)
print("Response:", response.text[:2000])