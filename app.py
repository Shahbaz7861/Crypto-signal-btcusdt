import streamlit as st
import requests
import numpy as np
from bs4 import BeautifulSoup
from sklearn.ensemble import RandomForestClassifier

# === Fetch Blockchain Metrics ===

# Fetch Bitcoin price from CoinGecko
def fetch_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return data['bitcoin']['usd']
    except Exception as e:
        st.error(f"Error fetching price: {e}")
        return None

# Fetch 24-hour volume for Bitcoin
def fetch_volume():
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin"
        response = requests.get(url)
        data = response.json()
        return data['market_data']['total_volume']['usd']
    except Exception as e:
        st.error(f"Error fetching volume: {e}")
        return None

# Fetch hash rate from CoinWarz
def fetch_hash_rate():
    try:
        url = "https://www.coinwarz.com/mining/bitcoin/hashrate-chart"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        hash_rate_tag = soup.find("span", {"id": "hashrate-value"})
        return float(hash_rate_tag.text.replace(",", "")) if hash_rate_tag else None
    except Exception as e:
        st.error(f"Error fetching hash rate: {e}")
        return None

# Fetch mining difficulty from CoinWarz
def fetch_difficulty():
    try:
        url = "https://www.coinwarz.com/mining/bitcoin/difficulty-chart"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        difficulty_tag = soup.find("span", {"id": "difficulty-value"})
        return float(difficulty_tag.text.replace(",", "")) if difficulty_tag else None
    except Exception as e:
        st.error(f"Error fetching difficulty: {e}")
        return None

# === Key Formulas ===

# 1. Weighted Probability Formula
def weighted_probability(weights, alpha=1):
    total = sum(w ** alpha for w in weights.values())
    probabilities = {k: (v ** alpha) / total for k, v in weights.items()}
    return probabilities

# 2. Momentum Prediction Formula
def momentum_prediction(prices):
    try:
        return [(prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))]
    except Exception as e:
        st.error(f"Error calculating momentum: {e}")
        return []

# 3. Weighted Price Prediction Formula
def weighted_price_prediction(prices, weights):
    try:
        return sum(p * w for p, w in zip(prices, weights)) / sum(weights)
    except Exception as e:
        st.error(f"Error calculating weighted price: {e}")
        return None

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
    try:
        net_sentiment = (long_positions - short_positions) / (long_positions + short_positions)
        return "Bullish" if net_sentiment > 0 else "Bearish"
    except ZeroDivisionError:
        return "Neutral"

# === Machine Learning Integration ===

def train_ml_model(features, labels):
    """
    Trains a Random Forest Classifier model on historical features and labels.
    """
    try:
        model = RandomForestClassifier()
        model.fit(features, labels)
        return model
    except Exception as e:
        st.error(f"Error training model: {e}")
        return None

def predict_signal(model, features):
    """
    Predicts a trading signal using a trained model.
    """
    try:
        return model.predict(features)
    except Exception as e:
        st.error(f"Error predicting signal: {e}")
        return None

# === Streamlit Interface ===
st.title("Advanced Crypto Signal Generator")

# Fetch metrics
price = fetch_price()
volume = fetch_volume()
hash_rate = fetch_hash_rate()
difficulty = fetch_difficulty()

# Display metrics
if price:
    st.write(f"**Price:** ${price} [Source: CoinGecko](https://www.coingecko.com)")
if volume:
    st.write(f"**Volume:** ${volume} [Source: CoinGecko](https://www.coingecko.com)")
if hash_rate:
    st.write(f"**Hash Rate:** {hash_rate} TH/s [Source: CoinWarz](https://www.coinwarz.com/mining/bitcoin/hashrate-chart)")
if difficulty:
    st.write(f"**Difficulty:** {difficulty} [Source: CoinWarz](https://www.coinwarz.com/mining/bitcoin/difficulty-chart)")

# Example Formulas
if price and volume and hash_rate and difficulty:
    # Weighted Probability
    probabilities = weighted_probability({"hash_rate": hash_rate, "difficulty": difficulty})
    st.write(f"**Weighted Probabilities:** {probabilities}")

    # Signal Generation
    signal = signal_generation(rsi=25, ema_short=price, ema_long=volume)  # Example RSI/EMA
    st.write(f"**Trading Signal:** {signal}")

    # Machine Learning Example
    st.subheader("Machine Learning Example")
    features = np.array([[price, volume, hash_rate, difficulty]])
    labels = ["Buy", "Sell"]  # Mock labels
    model = train_ml_model(features, labels)
    if model:
        prediction = predict_signal(model, features)
        st.write(f"**ML Predicted Signal:** {prediction[0]}")
else:
    st.error("Failed to fetch all required metrics. Please check your API connections.")

# Reference Links
st.write("### Reference Links")
st.markdown("""
- [CoinGecko API Documentation](https://www.coingecko.com/en/api/documentation)
- [CoinWarz Hash Rate Chart](https://www.coinwarz.com/mining/bitcoin/hashrate-chart)
- [CoinWarz Difficulty Chart](https://www.coinwarz.com/mining/bitcoin/difficulty-chart)
""")
    # Added app.py as signal generator
