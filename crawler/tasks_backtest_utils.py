import pandas as pd
import numpy as np
import pandas_ta as ta
import os

from crawler.worker import app

# 🎯 任務 1：計算各項技術指標（RSI, MA, MACD, KD）
@app.task()
def calculate_indicators(df):
    """
    對傳入的股價資料 DataFrame 計算技術分析指標，並回傳含技術指標的 DataFrame。
    指標包含：
    - RSI（14日）
    - 移動平均線（MA5, MA20）
    - MACD（快線、慢線、柱狀圖）
    - KD 隨機指標（%K, %D）
    """

    df = df.copy()

    # RSI (14) (相對強弱指標)
    df["RSI_14"] = ta.rsi(df["Close"], length=14)

    # MA5、MA20（移動平均線）（也可以使用 df['Close'].rolling(5).mean())）
    df["MA5"] = ta.sma(df["Close"], length=5)
    df["MA20"] = ta.sma(df["Close"], length=20)

    # MACD（移動平均收斂背離指標）
    macd = ta.macd(df["Close"], fast=12, slow=26, signal=9)
    df["MACD_line"] = macd["MACD_12_26_9"]
    df["MACD_signal"] = macd["MACDs_12_26_9"]
    df["MACD_hist"] = macd["MACDh_12_26_9"]

    # KD 指標（STOCH: 隨機震盪指標）
    stoch = ta.stoch(df["High"], df["Low"], df["Close"], k=14, d=3, smooth_k=3)
    df["%K"] = stoch["STOCHk_14_3_3"]
    df["%D"] = stoch["STOCHd_14_3_3"]

    return df

# 🎯 任務 2：計算策略績效評估指標
@app.task()
def evaluate_performance(df):
    """
    根據含 Adj_Close 的股價資料，計算回測績效指標並以 dict 回傳：
    - 總報酬率（Total Return）
    - 年化報酬率（CAGR）
    - 最大回撤（Max Drawdown）
    - 夏普比率（Sharpe Ratio）
    """
    # 基本防呆
    if df is None or df.empty or "Adj_Close" not in df.columns:
        return None

    # 總報酬率（Total Return）
    df['Return'] = df['Adj_Close'].pct_change()
    df['Cumulative'] = (1 + df['Return']).cumprod()
    # 若 Cumulative 無有效數值，則跳過
    if df['Cumulative'].isnull().all():
        return None
    # 若資料不足，或無法取得開始/結束日期
    if df.index.empty or df['Cumulative'].isna().iloc[-1]:
        return None
    total_return = df['Cumulative'].iloc[-1] - 1

    # 年化報酬率（CAGR）
    days = (df.index[-1] - df.index[0]).days
    if days <= 0 or df['Cumulative'].iloc[-1] <= 0:
        cagr = np.nan
    else:
        cagr = df['Cumulative'].iloc[-1] ** (365 / days) - 1

    # 最大回撤（Max Drawdown）
    roll_max = df['Cumulative'].cummax()
    drawdown = df['Cumulative'] / roll_max - 1
    max_drawdown = drawdown.min()

    # 夏普比率（Sharpe Ratio）
    std_return = df['Return'].std()
    sharpe = np.sqrt(252) * df['Return'].mean() / std_return if std_return and std_return != 0 else np.nan

    # 清理暫存欄
    df.drop(columns=["Return", "Cumulative"], inplace=True)

    return {
        "Total Return": total_return,
        "CAGR": cagr,
        "Max Drawdown": max_drawdown,
        "Sharpe Ratio": sharpe
    }

