import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
tickers = [
           'ASTS', 
           'ORR', 
           'GOOG',
           'META', 
           'AMZN',
           'DBSDY', 
           'CB', 
           'BN', 
           'GEV', 
           'KSPI', 
           'TMDX', 
           'ILMN', 
           'HOOD', 
           'RDDT', 
           'JD', 
           'KRUS', 
           'PDD', 
           'MELI',
           'CRM', 
           'INTU', 
           'ADBE',
           'SPY'
           ]

prices = yf.download(tickers, start='2023-01-01', auto_adjust=True)['Close']
prices = prices[tickers] 

returns = prices.pct_change(fill_method=None)
corr_matrix = returns.corr()

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