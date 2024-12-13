# 1. Weighted Probability Formula
def weighted_probability(weights, alpha=1):
    """
    Calculate weighted probabilities using given weights and alpha.
    """
    total = sum(w ** alpha for w in weights.values())
    return {k: (v ** alpha) / total for k, v in weights.items()}

# 2. Momentum Prediction Formula
def momentum_prediction(prices):
    """
    Calculate price momentum as the relative difference between current and previous prices.
    """
    return [(prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))]

# 3. Signal Generation Formula
def signal_generation(rsi, ema_short, ema_long):
    """
    Generate buy/sell/hold signals based on RSI and EMA crossover.
    """
    if rsi < 30 and ema_short > ema_long:
        return "Buy"
    elif rsi > 70 and ema_short < ema_long:
        return "Sell"
    else:
        return "Hold"

# 4. Long/Short Position Analysis Formula
def long_short_analysis(long_positions, short_positions):
    """
    Analyze market sentiment based on long and short positions.
    """
    net_sentiment = (long_positions - short_positions) / (long_positions + short_positions)
    return "Bullish" if net_sentiment > 0 else "Bearish"

# 5. Price Prediction Formula
def price_prediction(prices, weights):
    """
    Predict future price using weighted averages of historical prices.
    """
    return sum(p * w for p, w in zip(prices, weights)) / sum(weights)

# Additional Formulas for Hash Rate and Difficulty

def calculate_mining_pressure(hashrate, difficulty):
    """
    Calculate mining pressure as a ratio of hash rate to difficulty.
    """
    try:
        return hashrate / difficulty if difficulty > 0 else 0
    except ZeroDivisionError:
        return 0

def calculate_signals(data, hashrate, difficulty, vw, pw, bw, mt, ss):
    """
    Generate trading signals integrating hash rate, difficulty, and mining pressure.
    """
    # Mining pressure
    mining_pressure = calculate_mining_pressure(hashrate, difficulty)
    data["mining_pressure"] = mining_pressure

    # Weighted Probability Formula (updated with mining pressure)
    data["probability"] = (vw * data["volume"] + pw * data["price"] + bw * mining_pressure) / (vw + pw + bw)

    # Momentum Prediction Formula
    data["momentum"] = data["price"].diff().rolling(5).mean() / data["price"]

    # Signal Generation (example: Buy, Sell, or Hold)
    data["long_signal"] = data["momentum"] > mt
    data["short_signal"] = data["momentum"] < -mt
    data["scalp_long"] = abs(data["price"] - data["price"].rolling(14).min()) / data["price"].rolling(14).min() < ss
    data["scalp_short"] = abs(data["price"] - data["price"].rolling(14).max()) / data["price"].rolling(14).max() < ss

    # Combine buy/sell signals
    data["buy_signal"] = data["long_signal"] & data["scalp_long"]
    data["sell_signal"] = data["short_signal"] & data["scalp_short"]

    return data
