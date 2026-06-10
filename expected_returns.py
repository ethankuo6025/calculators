import yfinance as yf
import seaborn as sns
import numpy as np

tickers = ['UPRO', 'SPY', 'SPXU', 'GOOG', 'ASTS']
prices = yf.download(tickers, start='2024-01-01', auto_adjust=True)['Close']
returns = prices.pct_change(fill_method=None).dropna()

weights = np.array([.2, .2, .2, .2, .2])
cov_matrix = returns.cov().values * 252 
portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
portfolio_volatility = np.sqrt(portfolio_variance)

avg_daily_returns = returns.mean()
annualized_returns = avg_daily_returns * 252
portfolio_expected_return = np.dot(weights, annualized_returns)

print(f"Portfolio Volatility: {portfolio_volatility}")
print(f"Expected Returns: {portfolio_expected_return}")
