"""
demo of the beta/corr/vol screener
"""

import pandas as pd
from src import config
from src.helpers import calculate_beta

# examples
tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "META", "NVDA", "JPM", "V",
    "UNH", "XOM", "JNJ", "PG"]

benchmark = [config.SP500]
start = "2023-01-01"

corr_matrix, beta_matrix, vol_matrix = calculate_beta(tickers, benchmark, start)

for bench in benchmark:
    metrics = pd.DataFrame({
        "beta": beta_matrix[bench],
        "corr": corr_matrix[bench],
        "vol_ratio": vol_matrix[bench],
    })

    print(f"\n=== Benchmark: {bench} ===")
    print(metrics.sort_values("beta"))
