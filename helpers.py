import numpy as np
from pandas import DataFrame, Series
from data import get_prices

def _get_returns(tickers: list[str], benchmark: list[str] | str, start: str) -> tuple[DataFrame, list[str], list[str]]:
    """returns daily returns alongside the ticker/benchmark lists with invalid names dropped"""
    if isinstance(benchmark, str):
        benchmark = [benchmark]
    prices = get_prices(tickers + benchmark, start=start)

    returns = prices.pct_change(fill_method=None)

    # drop invalid tickers
    missing = [t for t in tickers + benchmark if t not in returns.columns]
    if missing:
        print(f"Skipping invalid/missing tickers: {missing}")

    tickers = [t for t in tickers if t in returns.columns]
    benchmark = [t for t in benchmark if t in returns.columns]
    return returns, tickers, benchmark

def calculate_beta(tickers: list[str], benchmark: list[str] | str, start: str) -> tuple[DataFrame, DataFrame, DataFrame]:
    """returns 3 dataframes: correlation, beta, and volatility Matrices"""
    returns, tickers, benchmark = _get_returns(tickers, benchmark, start)

    ticker_std = returns[tickers].std()
    benchmark_std = returns[benchmark].std()

    corr_matrix = returns.corr().loc[tickers, benchmark] # index=tickers, columns=benchmarks
    beta_matrix = corr_matrix.mul(ticker_std, axis=0).div(benchmark_std, axis=1)
    vol_matrix = beta_matrix.div(corr_matrix)
    return corr_matrix, beta_matrix, vol_matrix

def calculate_factor_covariance(
    tickers: list[str],
    benchmark: list[str] | str,
    start: str,
    multivariate: bool = True,
) -> DataFrame:
    """returns the noise-filtered NxN covariance matrix, Sigma = B F B.T + D

    B = NxK beta matrix
    F = KxK factor covariance
    D = diagonal of residual variances
    multivariate=False uses calculate_beta's univariate betas,
    which double-count correlated benchmarks and flatten D to zero.
    """
    returns, tickers, benchmark = _get_returns(tickers, benchmark, start)

    aligned = returns[tickers + benchmark].dropna()
    assets, factors = aligned[tickers], aligned[benchmark]

    if multivariate:
        assets_centered = assets - assets.mean()
        factors_centered = factors - factors.mean()
        B = DataFrame(
            np.linalg.solve(
                factors_centered.T @ factors_centered,
                factors_centered.T @ assets_centered,
            ).T,
            index=tickers,
            columns=benchmark,
        )
    else:
        corr = aligned.corr().loc[tickers, benchmark]
        B = corr.mul(assets.std(), axis=0).div(factors.std(), axis=1)

    F = factors.cov()

    common = B @ F @ B.T
    residual_var = (assets.var() - np.diag(common)).clip(lower=0)

    return common + DataFrame(np.diag(residual_var), index=tickers, columns=tickers)

def prune_benchmark(arr: list[str], benchmark: str) -> Series:
    return arr[benchmark]