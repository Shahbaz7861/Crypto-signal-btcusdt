import requests
from bs4 import BeautifulSoup

# === Fetch Hash Rate and Difficulty ===
def fetch_hash_rate_and_difficulty():
    # URLs for hash rate and difficulty
    url_hashrate = "https://www.coinwarz.com/mining/bitcoin/hashrate-chart"
    url_difficulty = "https://www.coinwarz.com/mining/bitcoin/difficulty-chart"

    # Fetch responses
    response_hashrate = requests.get(url_hashrate)
    response_difficulty = requests.get(url_difficulty)

    # Parse HTML to extract data
    hash_rate = parse_hashrate_from_html(response_hashrate.text)
    difficulty = parse_difficulty_from_html(response_difficulty.text)

    return hash_rate, difficulty

# === Parsing Logic for Hash Rate ===
def parse_hashrate_from_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    try:
        # Adjust the selector based on CoinWarz page structure
        hash_rate_tag = soup.find("div", {"class": "stats-card"})  # Example selector
        hash_rate = hash_rate_tag.find("h3").text.strip() if hash_rate_tag else None
        return hash_rate
    except Exception as e:
        return f"Error parsing hash rate: {e}"

# === Parsing Logic for Difficulty ===
def parse_difficulty_from_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    try:
        # Adjust the selector based on CoinWarz page structure
        difficulty_tag = soup.find("div", {"class": "stats-card"})  # Example selector
        difficulty = difficulty_tag.find("h3").text.strip() if difficulty_tag else None
        return difficulty
    except Exception as e:
        return f"Error parsing difficulty: {e}"
    # Added app.py as signal generator
