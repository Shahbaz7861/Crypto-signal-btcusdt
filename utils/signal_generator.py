from strategies.scalping import scalping_strategy
from strategies.long_short import long_short_strategy

def generate_final_signals(data, scalping_sensitivity, momentum_threshold):
    """
    Combine scalping and long/short strategies into final signals.
    """
    scalping_signals = scalping_strategy(data, scalping_sensitivity)
    long_short_signals = long_short_strategy(data, momentum_threshold)

    # Combine strategies into final buy/sell signals
    data["scalping_signal"] = scalping_signals
    data["long_short_signal"] = long_short_signals
    data["buy_signal"] = data["scalping_signal"] & data["long_short_signal"]
    data["sell_signal"] = ~data["scalping_signal"] & ~data["long_short_signal"]

    return data
