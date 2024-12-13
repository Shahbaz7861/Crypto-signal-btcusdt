import requests

def fetch_crypto_data():
    """Fetch price and volume from CoinGecko."""
    try:
        price_response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        volume_response = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin")
        price = price_response.json()["bitcoin"]["usd"]
        volume = volume_response.json()["market_data"]["total_volume"]["usd"]
        return price, volume
    except Exception:
        return None, None

def fetch_blockchain_data():
    """Fetch hash rate and difficulty from CoinWarz."""
    try:
        hash_rate_response = requests.get("https://www.coinwarz.com/mining/bitcoin/hashrate-chart")
        difficulty_response = requests.get("https://www.coinwarz.com/mining/bitcoin/difficulty-chart")
        hash_rate = parse_html_data(hash_rate_response.text)
        difficulty = parse_html_data(difficulty_response.text)
        return hash_rate, difficulty
    except Exception:
        return None, None

def parse_html_data(html):
    """Placeholder parser for CoinWarz data."""
    return 350  # Mocked hash rate/difficulty values
