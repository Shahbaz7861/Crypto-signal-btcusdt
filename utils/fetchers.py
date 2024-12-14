import streamlit as st
import requests

# --- Fetch Functions ---

def fetch_mempool_transaction_count():
    """
    Fetch transaction count from Mempool API.
    Returns:
        int: Transaction count.
    """
    try:
        st.write("Fetching Mempool Transaction Count...")
        response = requests.get("https://mempool.space/api/mempool")
        if response.status_code == 200:
            data = response.json()
            st.success("Transaction Count Fetched Successfully!")
            return data.get("count", None)
        else:
            st.error(f"Failed to fetch Mempool transaction count. Status Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching Mempool transaction count: {e}")
        return None


def fetch_blockchain_difficulty():
    """
    Fetch mining difficulty from Blockchain.com API.
    Returns:
        float: Mining difficulty.
    """
    try:
        st.write("Fetching Blockchain Difficulty...")
        response = requests.get("https://blockchain.info/q/getdifficulty")
        if response.status_code == 200:
            difficulty = response.json()
            st.success("Blockchain Difficulty Fetched Successfully!")
            return difficulty
        else:
            st.error(f"Failed to fetch Blockchain difficulty. Status Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching Blockchain Difficulty: {e}")
        return None


def fetch_blockchain_hashrate():
    """
    Fetch hash rate from Blockchain.com API.
    Returns:
        float: Hash rate.
    """
    try:
        st.write("Fetching Blockchain Hash Rate...")
        response = requests.get("https://blockchain.info/q/hashrate")
        if response.status_code == 200:
            hashrate = response.json()
            st.success("Blockchain Hash Rate Fetched Successfully!")
            return hashrate
        else:
            st.error(f"Failed to fetch Blockchain hash rate. Status Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching Blockchain Hash Rate: {e}")
        return None


def fetch_binance_price_data():
    """
    Fetch price data from Binance API with debugging.
    Returns:
        list: Binance candlestick data for BTC/USDT.
    """
    try:
        st.write("Fetching Binance Price Data...")
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": "BTCUSDT", "interval": "1m", "limit": 15}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            st.success("Binance Price Data Fetched Successfully!")
            return response.json()
        elif response.status_code == 451:
            st.error("Binance API is unavailable in your region (451 error). Try using a VPN or alternative API.")
            return None
        else:
            st.error(f"Failed to fetch Binance price data. Status Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching Binance Price Data: {e}")
        return None


def fetch_binance_order_book():
    """
    Fetch order book data from Binance API with debugging.
    Returns:
        dict: Order book data (bids and asks) for BTC/USDT.
    """
    try:
        st.write("Fetching Binance Order Book...")
        url = "https://api.binance.com/api/v3/depth"
        params = {"symbol": "BTCUSDT", "limit": 10}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            st.success("Binance Order Book Fetched Successfully!")
            return {
                "bids": response.json()["bids"],
                "asks": response.json()["asks"],
            }
        elif response.status_code == 451:
            st.error("Binance API is unavailable in your region (451 error). Try using a VPN or alternative API.")
            return None
        else:
            st.error(f"Failed to fetch Binance Order Book. Status Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching Binance Order Book: {e}")
        return None


def fetch_price_data_with_fallback():
    """
    Fetch price data using Binance as primary and CoinGecko as fallback.
    Returns:
        list: Price data in a compatible format.
    """
    # Try Binance API first
    price_data = fetch_binance_price_data()
    if price_data:
        return price_data

    # If Binance fails, fallback to CoinGecko
    st.warning("Falling back to CoinGecko for price data...")
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        if response.status_code == 200:
            st.success("Price Data Fetched from CoinGecko!")
            return [{"close": response.json()["bitcoin"]["usd"]}]
        else:
            st.error(f"Failed to fetch price data from CoinGecko. Status Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching price data from CoinGecko: {e}")
        return None


def fetch_order_book_with_fallback():
    """
    Fetch order book data using Binance as primary and simulated data as fallback.
    Returns:
        dict: Order book data (bids and asks).
    """
    # Try Binance API first
    order_book = fetch_binance_order_book()
    if order_book:
        return order_book

    # Fallback to simulated data
    st.warning("Using simulated order book data...")
    return {
        "bids": [["10100.00", "0.5"], ["10099.00", "0.3"]],  # Example bids
        "asks": [["10101.00", "0.4"], ["10102.00", "0.2"]],  # Example asks
    }


def fetch_combined_metrics():
    """
    Fetch and consolidate data from multiple APIs.
    Returns:
        dict: Consolidated metrics (transaction count, difficulty, hash rate, price data, and order book).
    """
    transaction_count = fetch_mempool_transaction_count()
    difficulty = fetch_blockchain_difficulty()
    hash_rate = fetch_blockchain_hashrate()
    price_data = fetch_price_data_with_fallback()  # Use fallback fetcher for price
    order_book = fetch_order_book_with_fallback()  # Use fallback fetcher for order book

    if (
        transaction_count is not None and difficulty is not None 
        and hash_rate is not None and price_data is not None 
        and order_book is not None
    ):
        st.success("All Data Fetched Successfully!")
        return {
            "transaction_count": transaction_count,
            "difficulty": difficulty,
            "hash_rate": hash_rate,
            "price_data": price_data,
            "order_book": order_book,
        }
    else:
        st.warning("Failed to fetch some data sources. Check above for errors.")
        return None
