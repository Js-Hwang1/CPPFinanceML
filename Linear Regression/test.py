import yfinance as yf
import pandas as pd

# Fetch historical stock data
stock = yf.Ticker('^NDX')
df = stock.history(start='2010-01-01', end='2024-07-01')

# Check if the dataframe is empty
if df.empty:
    print("No price data found for the ticker symbol.")
else:
    # Prepare the data
    df = df.drop(columns=['Dividends', 'Stock Splits'])
    df['td_D'] = ((df['Close'] - df['Open']) / df['Open']) * 100
    df['yd_D'] = (df['td_D'].shift(1)+df['td_D'].shift(2)+df['td_D'].shift(3)+df['td_D'].shift(4)+df['td_D'].shift(5))/5
    df.dropna(inplace=True)
    df = df[['td_D', 'yd_D']]  # Only keep relevant columns

    # Calculate means
    X_bar = df['yd_D'].mean()
    Y_bar = df['td_D'].mean()

    # Calculate beta1 and beta0
    covariance = ((df['yd_D'] - X_bar) * (df['td_D'] - Y_bar)).sum()
    variance = ((df['yd_D'] - X_bar) ** 2).sum()

    beta1 = covariance / variance
    beta0 = Y_bar - beta1 * X_bar

    # Calculate residuals and RSE
    n = df.shape[0]
    residuals = df['td_D'] - (beta0 + beta1 * df['yd_D'])
    RSE = (residuals**2).sum() / (n - 2)
    RSE = RSE**0.5

    # Calculate TSS
    TSS = ((df['td_D'] - Y_bar) ** 2).sum()

    # Calculate R^2
    Rsq = 1 - (RSE**2 / TSS)

    print(f'R^2 = {Rsq:.4f}')
    print(f'beta1 = {beta1:.4f}')
    print(f'beta0 = {beta0:.4f}')
