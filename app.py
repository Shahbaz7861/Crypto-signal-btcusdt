import streamlit as st
from utils.fetchers import fetch_combined_metrics
from utils.signal_generator import generate_signals
import pandas as pd

# Streamlit page configuration
st.set_page_config(page_title="Trading Signal Generator", layout="wide")

# App title
st.title("📈 Trading Signal Generator")
st.markdown("Analyze market data and generate real-time trading signals based on advanced metrics.")

# Step 1: Fetch Data
st.header("Step 1: Fetch Market Data")
if st.button("Fetch Data"):
    st.write("Fetching data from APIs...")
    combined_data = fetch_combined_metrics()

    if combined_data:
        st.success("Data fetched successfully!")

        # Extract metrics from combined data
        price_data = combined_data["price_data"]
        difficulty = combined_data["difficulty"]
        hashrate = combined_data["hash_rate"]

        # Step 2: Preprocess Price Data
        df = pd.DataFrame(
            price_data,
            columns=[
                "open_time", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "num_trades",
                "taker_buy_base", "taker_buy_quote", "ignore",
            ],
        )
        df["price"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)

        st.subheader("Market Data (Preprocessed)")
        st.dataframe(df.head(), width=900, height=300)

        # Step 3: Define Signal Parameters
        st.header("Step 2: Configure Signal Parameters")
        vw = st.slider("Weight for Volume (VW)", 0.0, 1.0, 0.3)
        pw = st.slider("Weight for Price (PW)", 0.0, 1.0, 0.4)
        bw = st.slider("Weight for Mining Pressure (BW)", 0.0, 1.0, 0.3)
        mt = st.number_input("Momentum Threshold (MT)", value=0.01, step=0.01)
        ss = st.number_input("Scalping Threshold (SS)", value=0.05, step=0.01)

        # Step 4: Generate Signals
        st.header("Step 3: Generate Trading Signals")
        if st.button("Generate Signals"):
            st.write("Generating signals...")
            try:
                signals = generate_signals(df, hashrate, difficulty, vw, pw, bw, mt, ss)
                st.success("Signals generated successfully!")

                # Display Signals
                st.subheader("Trading Signals")
                st.dataframe(signals[["price", "momentum", "buy_signal", "sell_signal"]], width=900, height=300)

                # Download Signals
                csv = signals.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Signal Data as CSV",
                    data=csv,
                    file_name="trading_signals.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"Error generating signals: {e}")
    else:
        st.error("Failed to fetch data. Please check your API connections or logs.")

st.write("---")
st.markdown("**Developed for interactive market analysis and decision-making.**")
