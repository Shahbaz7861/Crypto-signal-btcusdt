import streamlit as st
import requests
from bs4 import BeautifulSoup  # Required for parsing HTML
import logging

# === Setup Logging ===
logging.basicConfig(level=logging.INFO)

# === Fetch Hash Rate and Difficulty ===
def fetch_hash_rate_and_difficulty():
    # URLs for hash rate and difficulty
    url_hashrate = "https://www.coinwarz.com/mining/bitcoin/hashrate-chart"
    url_difficulty = "https://www.coinwarz.com/mining/bitcoin/difficulty-chart"

    # Fetch responses
    response_hashrate = requests.get(url_hashrate)
    response_difficulty = requests.get(url_difficulty)

    # Log raw HTML responses for debugging
    logging.info(f"Hash Rate Response HTML: {response_hashrate.text[:500]}")  # Show first 500 chars
    logging.info(f"Difficulty Response HTML: {response_difficulty.text[:500]}")  # Show first 500 chars

    # Parse HTML to extract data
    hash_rate = parse_hashrate_from_html(response_hashrate.text)
    difficulty = parse_difficulty_from_html(response_difficulty.text)

    return hash_rate, difficulty

# === Parsing Logic for Hash Rate ===
def parse_hashrate_from_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    # Example: Locate the specific tag containing hash rate data
    try:
        hash_rate_tag = soup.find("div", {"class": "chart-value"})  # Adjust this selector
        hash_rate = hash_rate_tag.text.strip() if hash_rate_tag else None
        return hash_rate
    except Exception as e:
        logging.error(f"Error parsing hash rate: {e}")
        return None

# === Parsing Logic for Difficulty ===
def parse_difficulty_from_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    # Example: Locate the specific tag containing difficulty data
    try:
        difficulty_tag = soup.find("div", {"class": "chart-value"})  # Adjust this selector
        difficulty = difficulty_tag.text.strip() if difficulty_tag else None
        return difficulty
    except Exception as e:
        logging.error(f"Error parsing difficulty: {e}")
        return None

# === Streamlit Interface ===
st.title("Advanced Crypto Signal Generator")

# Fetch metrics
try:
    hash_rate, difficulty = fetch_hash_rate_and_difficulty()
    st.write(f"Hash Rate: {hash_rate}")
    st.write(f"Difficulty: {difficulty}")
except Exception as e:
    st.error(f"Failed to fetch hash rate or difficulty: {e}")

# Reference Links
st.markdown("### Reference Links")
st.markdown("- [CoinWarz Hash Rate Chart](https://www.coinwarz.com/mining/bitcoin/hashrate-chart)")
st.markdown("- [CoinWarz Difficulty Chart](https://www.coinwarz.com/mining/bitcoin/difficulty-chart)")
    # Added app.py as signal generator
