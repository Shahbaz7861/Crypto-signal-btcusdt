import streamlit as st
from utils.fetchers import fetch_hashrate, fetch_difficulty, fetch_price, fetch_mock_market_data
from utils.formulas import weighted_probability, momentum_prediction, price_prediction
from utils.signal_generator import generate_signals
import logging
import pandas as pd

# Setup logging
logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s - %(message)s")
logging.info("App initialized")

# App Title
st.title("Crypto Signals BTC/USDT Dashboard")

# Sidebar Parameters
st.sidebar.header("Adjust Formula Parameters")
volume_weight = st.sidebar.slider("Volume Weight", 0.1, 1.0, 0.5)
price_weight = st.sidebar.slider("Price Weight", 0.1, 1.0, 0.4)
blockchain_weight = st.sidebar.slider("Blockchain Weight", 0.1, 1.0, 0.1)
momentum_threshold = st.sidebar.slider("Momentum Threshold", 0.01, 0.5, 0.1)
scalping_sensitivity = st.sidebar.slider("Scalping Sensitivity", 0.01, 0.2, 0.05)

# Display Mining and Market Data
st.header("Mining and Market Data")
hashrate = fetch_hashrate()
difficulty = fetch_difficulty()
price = fetch_price()

if isinstance(hashrate, dict) and "error" in hashrate:
    st.error(hashrate["error"])
else:
    st.write(f"**Hash Rate:** {hashrate} EH/s")

if isinstance(difficulty, dict) and "error" in difficulty:
    st.error(difficulty["error"])
else:
    st.write(f"**Difficulty:** {difficulty}")

if isinstance(price, dict) and "error" in price:
    st.error(price["error"])
else:
    st.write(f"**Price:** ${price:.2f}")

# Fetch and Display Live Market Data
st.header("Live Market Data and Trading Signals")
if st.button("Fetch Live Data"):
    try:
        # Fetch mock market data
        market_data = fetch_mock_market_data()

        # Generate trading signals
        signals = generate_signals(
            market_data,
            hashrate=hashrate,
            difficulty=difficulty,
            vw=volume_weight,
            pw=price_weight,
            bw=blockchain_weight,
            mt=momentum_threshold,
            ss=scalping_sensitivity
        )

        # Display signals
        st.subheader("Trading Signals")
        st.dataframe(signals)
    except Exception as e:
        st.error(f"Error generating signals: {e}")

# Historical Data Section
st.header("Historical Data")
if st.button("Fetch Historical Data"):
    try:
        # Example historical data (replace with actual fetch logic)
        historical_data = pd.read_csv("data/historical.csv")
        st.write(historical_data.head())
    except Exception as e:
        st.error(f"Error fetching historical data: {e}")
