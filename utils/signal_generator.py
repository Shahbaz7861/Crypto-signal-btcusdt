def generate_signals(data, hashrate, difficulty, vw, pw, bw, mt, ss):
    """Generate trading signals with mining and market data."""
    # Mining pressure
    mining_pressure = hashrate / difficulty if difficulty > 0 else 0

    # Weighted probability
    data["probability"] = (vw * data["volume"] + pw * data["price"] + bw * mining_pressure) / (vw + pw + bw)

    # Momentum
    data["momentum"] = data["price"].diff().rolling(5).mean() / data["price"]

        # Scalping signals
    data["scalp_long"] = abs(data["price"] - data["price"].rolling(14).min()) / data["price"].rolling(14).min() < ss
    data["scalp_short"] = abs(data["price"] - data["price"].rolling(14).max()) / data["price"].rolling(14).max() < ss

    # Long/Short signals
    data["long_signal"] = data["momentum"] > mt
    data["short_signal"] = data["momentum"] < -mt

    # Final Buy/Sell signals
    data["buy_signal"] = data["long_signal"] & data["scalp_long"]
    data["sell_signal"] = data["short_signal"] & data["scalp_short"]

    return data
