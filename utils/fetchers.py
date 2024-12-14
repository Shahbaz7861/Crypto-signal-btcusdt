import streamlit as st
import requests
import pandas as pd
import numpy as np

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
            st.error(f"Failed to fetch difficulty. Status Code: {response.status_code}")
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
            st.error(f"Failed to fetch hash rate. Status Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching Blockchain Hash Rate: {e}")
        return None


def fetch_binance_price_data():
    """
    Fetch price data from Binance API.
    Returns:
        list: Binance candlestick data.
    """
    try:
        st.write("Fetching Binance Price Data...")
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": "BTCUSDT", "interval": "1m", "limit": 15}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            st.success("Binance Price Data Fetched Successfully!")
            return data
        else:
            st.error(f"Failed to fetch Binance price data. Status Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching Binance Price Data: {e}")
        return None


def fetch_binance_order_book():
    """
    Fetch order book data from Binance API.
    Returns:
        dict: Order book data (bids and asks).
    """
    try:
        st.write("Fetching Binance Order Book...")
        url = "https://api.binance.com/api/v3/depth"
        params = {"symbol": "BTCUSDT", "limit": 10}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            st.success("Binance Order Book Fetched Successfully!")
            return {
                "bids": data["bids"],
                "asks": data["asks"]
            }
        else:
            st.error(f"Failed to fetch Binance Order Book. Status Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching Binance Order Book: {e}")
        return None


def fetch_combined_metrics():
    """
    Fetch and consolidate data from multiple APIs.
    Returns:
        dict: Consolidated metrics (transaction count, difficulty, hash rate, price data, and order book).
    """
    transaction_count = fetch_mempool_transaction_count()
    difficulty = fetch_blockchain_difficulty()
    hash_rate = fetch_blockchain_hashrate()
    price_data = fetch_binance_price_data()
    order_book = fetch_binance_order_book()

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


# --- Streamlit App Layout ---
st.title("Crypto Data Fetcher & Debugger")

# Fetch Data Button
if st.button("Fetch Data"):
    st.write("Fetching data from APIs...")
    combined_data = fetch_combined_metrics()

    if combined_data:
        st.write("### Fetched Data:")
        st.write(f"Transaction Count: {combined_data['transaction_count']}")
        st.write(f"Mining Difficulty: {combined_data['difficulty']}")
        st.write(f"Hash Rate: {combined_data['hash_rate']}")
        st.write("### Binance Price Data (First Entry):")
        st.write(combined_data["price_data"][:1])
        st.write("### Binance Order Book (Top Bids & Asks):")
        st.write(combined_data["order_book"])
    else:
        st.error("Failed to fetch all data.")
