"""
graphs_demo.py — archived, self-contained demo of the correlation-matrix plots.

This is a boilerplate version of graphs.py. It does NOT depend on the private
data layer (config / helpers / data / prices.db). Instead it generates synthetic
returns with a planted correlation structure so the plots run out-of-the-box:

    python archive/graphs_demo.py
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- demo inputs -----------------------------------------------------------
tickers = [f"ASSET{i:02d}" for i in range(12)]
start = "2023-01-01"
rng = np.random.default_rng(42)


# --- synthetic data --------------------------------------------------------
def make_demo_returns(names: list[str], n_days: int = 500) -> pd.DataFrame:
    """Daily returns with a couple of shared factors so clusters are visible."""
    n = len(names)
    # two latent factors each asset loads on with a random sign/strength
    loadings = rng.normal(size=(n, 2))
    factors = rng.normal(scale=0.01, size=(n_days, 2))
    idio = rng.normal(scale=0.008, size=(n_days, n))
    data = factors @ loadings.T + idio
    dates = pd.bdate_range(start=start, periods=n_days)
    return pd.DataFrame(data, columns=names, index=dates)


def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    """Plain NxN correlation matrix (stand-in for calculate_beta's corr output)."""
    return returns.corr()


def plot_clustermap(corr: pd.DataFrame, title: str) -> None:
    sns.clustermap(
        corr,
        cmap="RdBu_r",
        center=0,
        vmin=-1,
        vmax=1,
        annot=True,
        fmt=".2f",
        annot_kws={"size": 5},
        figsize=(12, 10),
        dendrogram_ratio=(0.15, 0.15),  # (Top Height Ratio, Left Width Ratio)
    )
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    returns = make_demo_returns(tickers)

    # NxN correlation
    corr_NxN = correlation_matrix(returns)
    plot_clustermap(corr_NxN, "NxN Correlation Matrix (demo)")

    # a "filtered" covariance-implied correlation: shrink toward the diagonal,
    # then convert the covariance back to a correlation for plotting.
    cov = returns.cov()
    shrunk = 0.7 * cov + 0.3 * np.diag(np.diag(cov))
    sigma = np.sqrt(np.diag(shrunk))
    corr_filtered = pd.DataFrame(
        shrunk.values / np.outer(sigma, sigma),
        index=cov.index,
        columns=cov.columns,
    )
    plot_clustermap(corr_filtered, "Filtered NxN Correlation Matrix (demo)")
