import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import config
from helpers import calculate_beta

tickers = [
    "VZ", "DHI", "T"
]
benchmark = config.BENCHMARK_LIST

corr_matrix, beta_matrix, vol_matrix = calculate_beta(tickers, benchmark)

plt.figure(figsize = (10, 8))
sns.heatmap(beta_matrix, 
            annot=True, 
            fmt='.2f',
            cmap='RdBu_r',
            center=0,
            vmin=-1, vmax=1,
            linewidths=.5)

plt.title('Asset Beta Matrix')
plt.show()

plt.figure(figsize = (10, 8))
sns.heatmap(corr_matrix, 
            annot=True, 
            fmt='.2f',
            cmap='RdBu_r',
            center=0,
            vmin=-1, vmax=1,
            linewidths=.5)

plt.title('Asset Correlation Matrix')
plt.show()

plt.figure(figsize = (10, 8))
sns.heatmap(vol_matrix, 
            annot=True, 
            fmt='.2f',
            cmap='RdBu_r',
            center=0,
            vmin=-1, vmax=1,
            linewidths=.5)

plt.title('Asset Volatility Matrix')
plt.show()