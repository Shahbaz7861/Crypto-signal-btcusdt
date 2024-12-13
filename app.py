import streamlit as st
import requests
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# === Fetch Blockchain Metrics ===
def fetch_hash_rate_and_difficulty():
    url = "https://blockchain.info/stats"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        hash_rate = data.get("hash_rate", None)
        difficulty = data.get("difficulty", None)
        return hash_rate, difficulty
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching hash rate and difficulty: {e}")
        return None, None
    except ValueError:
        st.error("Invalid JSON response from Blockchain API.")
        return None, None

def fetch_wallet_inflows(address):
    # Replace with your blockchain API endpoint or mock example
    return np.random.uniform(10, 100)  # Mock value for wallet inflows (replace with real API)

# === Crypto Data Fetching ===
def fetch_crypto_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data["price"]) if "price" in data else None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching crypto price: {e}")
        return None
    except ValueError:
        st.error("Invalid JSON response from Binance API.")
        return None

def fetch_crypto_volume():
    url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data["volume"]) if "volume" in data else None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching crypto volume: {e}")
        return None
    except ValueError:
        st.error("Invalid JSON response from Binance API.")
        return None

# === 5 Key Formulas ===
# 1. Weighted Probability Formula
def weighted_probability(weights, alpha=1):
    total = sum(w ** alpha for w in weights.values())
    probabilities = {k: (v ** alpha) / total for k, v in weights.items()}
    return probabilities

# 2. Momentum Prediction Formula
def momentum_prediction(prices):
    return [(prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))]

# 3. Price Prediction Formula
def weighted_price_prediction(prices, weights):
    return sum(p * w for p, w in zip(prices, weights)) / sum(weights)

# 4. Signal Generation Formula
def signal_generation(rsi, ema_short, ema_long):
    if rsi < 30 and ema_short > ema_long:
        return "Buy"
    elif rsi > 70 and ema_short < ema_long:
        return "Sell"
    else:
        return "Hold"

# 5. Long/Short Position Analysis Formula
def long_short_analysis(long_positions, short_positions):
    net_sentiment = (long_positions - short_positions) / (long_positions + short_positions)
    return "Bullish" if net_sentiment > 0 else "Bearish"

# === Machine Learning Integration ===
def train_ml_model(features, labels):
    model = RandomForestClassifier()
    model.fit(features, labels)
    return model

# === Streamlit Interface ===
st.title("Advanced Crypto Signal Generator")

# Fetch Metrics
price = fetch_crypto_price()
volume = fetch_crypto_volume()
hash_rate, difficulty = fetch_hash_rate_and_difficulty()

# Example Data for Machine Learning
if price and volume and hash_rate and difficulty:
    features = np.array([[price, volume, hash_rate, difficulty]])
    probabilities = weighted_probability({"hash_rate": hash_rate, "difficulty": difficulty})
    signal = signal_generation(25, price, volume)  # Example RSI and EMA
    st.write(f"Price: ${price}")
    st.write(f"Volume: {volume}")
    st.write(f"Hash Rate: {hash_rate}")
    st.write(f"Difficulty: {difficulty}")
    st.write(f"Signal: {signal}")
else:
    st.error("Failed to fetch required data. Please check your API connections.")
    # Added app.py as signal generator
