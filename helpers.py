from pandas import DataFrame
from data import get_prices

def calculate_beta(tickers: list[str], benchmark: list[str], start: str) -> tuple[DataFrame, DataFrame, DataFrame]:
    """returns 3 dataframes: correlation, beta, and volatility Matrices"""
    prices = get_prices(tickers + benchmark, start=start)

    returns = prices.pct_change(fill_method=None)

    # drop invalid tickers
    missing = [t for t in tickers + benchmark if t not in returns.columns]
    if missing:
        print(f"Skipping invalid/missing tickers: {missing}")

    tickers = [t for t in tickers if t in returns.columns]
    benchmark = [t for t in benchmark if t in returns.columns]

    ticker_std = returns[tickers].std()
    benchmark_std = returns[benchmark].std()

    corr_matrix = returns.corr().loc[tickers, benchmark] # index=tickers, columns=benchmarks
    beta_matrix = corr_matrix.mul(ticker_std, axis=0).div(benchmark_std, axis=1)
    vol_matrix = beta_matrix.div(corr_matrix)
    return corr_matrix, beta_matrix, vol_matrix