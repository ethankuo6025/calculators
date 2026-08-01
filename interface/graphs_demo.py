"""
demo of the correlation-matrix plots
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from src import config
from src.helpers import calculate_beta, calculate_factor_covariance

# examples
tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "META", "NVDA", "JPM", "V",
    "UNH", "XOM", "JNJ", "PG"]

benchmark = config.BENCHMARK_LIST
start = "2023-01-01"

# NxN correlation
corr_NxN, beta_NxN, vol_NxN = calculate_beta(tickers, tickers, start)

sns.clustermap(
    corr_NxN,
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

plt.title("NxN Correlation Matrix")
plt.show()

# filtered NxN (noise-filtered covariance, plotted as the correlation it implies)
cov_NxN = calculate_factor_covariance(tickers, benchmark, start)

sigma = np.sqrt(np.diag(cov_NxN))
corr_NxN = cov_NxN / np.outer(sigma, sigma)

sns.clustermap(
    corr_NxN,
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

plt.title("Filtered NxN Correlation Matrix")
plt.show()
