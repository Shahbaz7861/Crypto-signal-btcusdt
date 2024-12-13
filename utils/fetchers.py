import requests
from bs4 import BeautifulSoup


def fetch_hashrate():
    """
    Scrape Bitcoin hash rate from Coinwarz.
    """
    url = "https://www.coinwarz.com/mining/bitcoin/hashrate-chart"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        hashrate_data = soup.find("div", {"class": "m-chart-value"}).text.strip()
        hashrate = float(hashrate_data.replace(" EH/s", ""))  # Extract and convert to float
        return hashrate
    except Exception as e:
        return {"error": f"Error fetching hash rate: {e}"}


def fetch_difficulty():
    """
    Scrape Bitcoin difficulty from Coinwarz.
    """
    url = "https://www.coinwarz.com/mining/bitcoin/difficulty-chart"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        difficulty_data = soup.find("div", {"class": "m-chart-value"}).text.strip()
        difficulty = float(difficulty_data.replace(",", ""))  # Remove commas and convert to float
        return difficulty
    except Exception as e:
        return {"error": f"Error fetching difficulty: {e}"}


def fetch_price():
    """
    Scrape Bitcoin price from Coinwarz.
    """
    url = "https://www.coinwarz.com/prices/bitcoin/chart"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        price_data = soup.find("div", {"class": "m-chart-value"}).text.strip()
        price = float(price_data.replace("$", "").replace(",", ""))  # Remove $ and commas, then convert to float
        return price
    except Exception as e:
        return {"error": f"Error fetching price: {e}"}


def fetch_mining_data():
    """
    Scrape mining-related data from Coinwarz.
    """
    url = "https://www.coinwarz.com/mining/bitcoin"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Example: Find relevant mining data points (update these selectors based on the website structure)
        profit_tag = soup.find("span", {"id": "profit-label"})  # Example selector for profitability
        revenue_tag = soup.find("span", {"id": "revenue-label"})  # Example selector for revenue

        profitability = profit_tag.text.strip() if profit_tag else "N/A"
        revenue = revenue_tag.text.strip() if revenue_tag else "N/A"

        return {
            "profitability": profitability,
            "revenue": revenue
        }
    except Exception as e:
        return {"error": f"Error fetching mining data: {e}"}


def fetch_mock_market_data():
    """Mock function to simulate live market data."""
    try:
        data = pd.DataFrame({
            "price": [50000, 50150, 50200, 50250, 50300],  # Simulated price data
            "volume": [100, 200, 150, 300, 250],           # Simulated volume data
        })
        return data
    except Exception as e:
        return {"error": f"Mock market data fetch failed: {e}"}
