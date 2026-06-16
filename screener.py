import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import config
from helpers import calculate_beta
tickers = [
    "ASTS", "ORR", "GOOG", "AMZN", "META", "DBSDY", "CB", "BN", "KSPI", 
    "TMDX", "ILMN", "HOOD", "RDDT", "JD", "PDD", "CHTR", "KRUS", "MELI", 
    "CRM", "INTU", "ADBE", "ETH-USD", "INTC", "CBRS", "CRWV", "AMD", "ORCL"
]
benchmark = [config.SP500]

corr_matrix, beta_matrix, vol_matrix = calculate_beta(tickers, benchmark)

for bench in benchmark:
    metrics = pd.DataFrame({
        "beta": beta_matrix[bench],
        "corr": corr_matrix[bench],
        "vol_ratio": vol_matrix[bench],
    })

    print(f"\n=== Benchmark: {bench} ===")
    print(metrics.sort_values("beta"))
