import argparse
from typing import Tuple

import pandas as pd
import yfinance as yf


def _get_close_series(data: pd.DataFrame, symbol: str) -> pd.Series:
    """Return the close price series regardless of yfinance's column structure."""
    if isinstance(data.columns, pd.MultiIndex):
        return data[('Close', symbol)]
    return data['Close']


def fetch_price_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """Fetch historical price data for the given symbol using yfinance."""
    return yf.download(symbol, period=period)


def calculate_momentum(data: pd.DataFrame, symbol: str, window: int = 20) -> pd.DataFrame:
    """Calculate rolling percentage-change momentum."""
    data = data.copy()
    close = _get_close_series(data, symbol)
    data["momentum"] = close.pct_change(window)
    return data


def generate_signals(data: pd.DataFrame) -> pd.DataFrame:
    """Generate trading signals based on momentum."""
    data = data.copy()
    data["signal"] = 0
    data.loc[data["momentum"] > 0, "signal"] = 1
    data.loc[data["momentum"] <= 0, "signal"] = -1
    return data


def risk_management(price: float, stop_loss_pct: float = 0.05, take_profit_pct: float = 0.1) -> Tuple[float, float]:
    """Return stop-loss and take-profit levels for a given price."""
    stop_loss = price * (1 - stop_loss_pct)
    take_profit = price * (1 + take_profit_pct)
    return stop_loss, take_profit


def run(symbol: str, period: str = "1y", window: int = 20) -> None:
    """Execute the momentum trading workflow."""
    data = fetch_price_data(symbol, period)
    data = calculate_momentum(data, symbol, window)
    data = generate_signals(data)

    latest_close = _get_close_series(data, symbol).iloc[-1]
    stop_loss, take_profit = risk_management(latest_close)

    print(data[["Close", "momentum", "signal"]].tail())
    print(f"Stop Loss: {stop_loss:.2f}")
    print(f"Take Profit: {take_profit:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a simple momentum trading bot")
    parser.add_argument("symbol", help="Ticker symbol to trade")
    parser.add_argument("--period", default="1y", help="Historical period to download")
    parser.add_argument("--window", type=int, default=20, help="Momentum lookback window")
    args = parser.parse_args()
    run(args.symbol, period=args.period, window=args.window)


if __name__ == "__main__":
    main()

