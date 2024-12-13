# 1. Weighted Probability Formula
def weighted_probability(weights, alpha=1):
    total = sum(w ** alpha for w in weights.values())
    return {k: (v ** alpha) / total for k, v in weights.items()}

# 2. Momentum Prediction Formula
def momentum_prediction(prices):
    return [(prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))]

# 3. Signal Generation Formula
def signal_generation(rsi, ema_short, ema_long):
    if rsi < 30 and ema_short > ema_long:
        return "Buy"
    elif rsi > 70 and ema_short < ema_long:
        return "Sell"
    else:
        return "Hold"

# 4. Long/Short Position Analysis Formula
def long_short_analysis(long_positions, short_positions):
    net_sentiment = (long_positions - short_positions) / (long_positions + short_positions)
    return "Bullish" if net_sentiment > 0 else "Bearish"

# 5. Price Prediction Formula
def price_prediction(prices, weights):
    return sum(p * w for p, w in zip(prices, weights)) / sum(weights)
