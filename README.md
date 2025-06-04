# CODEXTEST

This repository shows how to build a simple momentum trading bot using Python. Below you'll find a fictional step-by-step guide. Feel free to adapt it to your own trading strategy.

## Requirements

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

## Strategy Overview

1. **Data Collection**: Fetch historical price data for your chosen asset using an API like `yfinance` or `pandas-datareader`.
2. **Momentum Calculation**: Calculate momentum as the percentage change over a rolling window (for example, 20 days).
3. **Signal Generation**: Enter a long position when momentum is positive and exit or short when momentum turns negative.
4. **Risk Management**: Set stop-loss and take-profit levels to manage risk.
5. **Automation**: Schedule the strategy with cron or a task scheduler to run periodically.

## Example Code Snippet

```python
import pandas as pd
import yfinance as yf

symbol = 'AAPL'
price_data = yf.download(symbol, period='1y')
price_data['momentum'] = price_data['Close'].pct_change(20)

price_data['signal'] = 0
price_data.loc[price_data['momentum'] > 0, 'signal'] = 1
price_data.loc[price_data['momentum'] <= 0, 'signal'] = -1

print(price_data[['Close', 'momentum', 'signal']].tail())
```

## Usage

Run the provided `momentum_bot.py` script to execute the same workflow from the
command line:

```bash
python momentum_bot.py AAPL --period 1y --window 20
```

This example downloads a year's worth of Apple stock data, computes 20-day momentum, and produces a basic trading signal.

## Disclaimer

This project is for educational purposes only. It does not constitute financial advice. Use at your own risk.

