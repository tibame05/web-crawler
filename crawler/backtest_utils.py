import pandas as pd
import numpy as np
import pandas_ta as ta
import os

from crawler.worker import app

@app.task()
def calculate_indicators(df):
    # RSI (相對強弱指標)
    df['RSI'] = ta.rsi(df['Close'], length=14)

    # MA5 和 MA20（也可以使用 ta.sma(df['Close'], length=5)）
    df['MA5'] = df['Close'].rolling(5).mean()
    df['MA20'] = df['Close'].rolling(20).mean()

    # MACD（移動平均收斂背離）
    macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_Signal'] = macd['MACDs_12_26_9']
    df['MACD_Hist'] = macd['MACDh_12_26_9']

    # KD 指標（STOCH: 隨機指標）
    stoch = ta.stoch(df['High'], df['Low'], df['Close'], k=14, d=3, smooth_k=3)
    df['%K'] = stoch['STOCHk_14_3_3']
    df['%D'] = stoch['STOCHd_14_3_3']

    return df

@app.task()
def evaluate_performance(df):
    df['Return'] = df['Adj_Close'].pct_change()
    df['Cumulative'] = (1 + df['Return']).cumprod()
    total_return = df['Cumulative'].iloc[-1] - 1

    days = (df.index[-1] - df.index[0]).days
    cagr = (df['Cumulative'].iloc[-1]) ** (365 / days) - 1 if days > 0 else np.nan

    roll_max = df['Cumulative'].cummax()
    drawdown = df['Cumulative'] / roll_max - 1
    max_drawdown = drawdown.min()

    sharpe = np.sqrt(252) * df['Return'].mean() / df['Return'].std() if df['Return'].std() != 0 else np.nan

    return {
        "Total Return": total_return,
        "CAGR": cagr,
        "Max Drawdown": max_drawdown,
        "Sharpe Ratio": sharpe
    }

