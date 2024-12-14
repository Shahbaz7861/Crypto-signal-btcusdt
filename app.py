from utils.fetchers import fetch_combined_metrics
from utils.formulas import calculate_signals
from utils.signal_generator import generate_signals
import logging
import pandas as pd

# Configure logging
logging.basicConfig(
    filename="app.log",  # Save logs in the same directory as the script
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def main():
    logging.info("=== Starting Application ===")

    # Step 1: Fetch data
    logging.info("Fetching data from APIs...")
    combined_data = fetch_combined_metrics()

    if not combined_data:
        logging.error("Failed to fetch data from APIs. Exiting application.")
        return

    logging.info("Data fetched successfully!")

    # Step 2: Extract fetched metrics
    price_data = combined_data["price_data"]
    difficulty = combined_data["difficulty"]
    hashrate = combined_data["hash_rate"]

    # Preprocess Binance price data
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

    logging.info("Price data processed into DataFrame.")

    # Step 3: Define weights and thresholds for calculations
    vw, pw, bw = 0.3, 0.4, 0.3  # Weights for volume, price, and mining pressure
    mt, ss = 0.01, 0.05  # Momentum and scalp thresholds

    # Step 4: Generate trading signals
    try:
        logging.info("Generating trading signals...")
        signals = generate_signals(df, hashrate, difficulty, vw, pw, bw, mt, ss)
        logging.info("Signals generated successfully!")
    except Exception as e:
        logging.error(f"Error generating signals: {e}")
        return

    # Step 5: Display results
    logging.info("Displaying generated signals...")
    print("=== Generated Signals ===")
    print(signals[["price", "momentum", "buy_signal", "sell_signal"]])
    logging.info("Application completed successfully.")

if __name__ == "__main__":
    main()
