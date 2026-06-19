import yfinance as yf
import numpy as np

tickers = ['UPRO', 'SPY', 'SPXU', 'GOOG', 'ASTS']
prices = yf.download(tickers, start='2024-01-01', auto_adjust=True)['Close']
returns = prices.pct_change(fill_method=None).dropna()

weights = np.array([.2, .2, .2, .2, .2])

asset_growth = prices / prices.iloc[0]
portfolio_value = asset_growth @ weights
portfolio_returns = portfolio_value.pct_change().dropna()

years = len(portfolio_returns) / 252
portfolio_expected_return = portfolio_value.iloc[-1] ** (1 / years) - 1

portfolio_volatility = portfolio_returns.std() * np.sqrt(252)

print(f"Historical CAGR: {portfolio_expected_return}")
print(f"Portfolio Volatility: {portfolio_volatility}")
