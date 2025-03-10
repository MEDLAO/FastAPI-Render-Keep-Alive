import os
from dotenv import load_dotenv
import requests
import schedule
import time


load_dotenv()

# List of public welcome endpoints for each API
API_ENDPOINTS = [
    "https://mycolorapi.p.rapidapi.com/",
    "https://myqrcodeapi1.p.rapidapi.com/",
    "https://myemailscraperapi.p.rapidapi.com/"
]

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# Headers including the API key
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "X-RapidAPI-Key": RAPIDAPI_KEY,
}


def ping_apis():
    """Send a GET request to each API's /welcome endpoint to prevent cold starts."""
    for url in API_ENDPOINTS:
        try:
            response = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=False)
            print(f"Pinged {url} - Status Code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error pinging {url}: {e}")


# Schedule the script to run every 5 minutes
schedule.every(5).minutes.do(ping_apis)

if __name__ == "__main__":
    print("Starting API keep-alive script...")
    ping_apis()  # Initial ping
    while True:
        schedule.run_pending()
        time.sleep(1)
