import pandas as pd
import numpy as np
import mplfinance as mpf
import talib # pylint: disable=no-member
import os
# print(talib.get_functions())

def calculate_indicators(df):
    # 計算 RSI 相對強弱指標（判斷過熱／超跌，RSI > 70 表示過熱，< 30 表示超跌）
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14) # 使用 14 日作為預設時間區間

    # 計算 MA5 / MA20 均線交叉策略（用於判斷黃金交叉，買進訊號：MA5 > MA20；或死亡交叉，賣出訊號：MA5 < MA20 ）
    df['MA5'] = df['Close'].rolling(5).mean()
    df['MA20'] = df['Close'].rolling(20).mean() #.rolling(n).mean() 計算 n 日移動平均

    # 計算 MACD 移動平均收斂背離（判斷多空趨勢轉折，MACD 線上穿訊號線 → 做多，MACD 線下穿訊號線 → 做空）
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = talib.MACD(df['Close'],
                                                                 fastperiod=12, slowperiod=26, signalperiod=9)
        #MACD：快線，MACD_Signal：慢線，MACD_Hist：柱狀圖（差距）
    
    # 計算 KD指標（判斷短期買賣點、轉折，如 %K < 20 表示超跌、可能進場，%K > 80 表示過熱、可能出場）
    df['%K'], df['%D'] = talib.STOCH(df['High'], df['Low'], df['Close'],
                                     fastk_period=14, slowk_period=3, slowd_period=3)
        # %K 是主線，%D 是平滑後的訊號線

    return df

def evaluate_performance(df):
    # 總報酬率（Total Return）
    df['Return'] = df['Adj_Close'].pct_change() # 每日報酬率（Return）：計算每一天相對於前一天的報酬率（百分比變化）
    df['Cumulative'] = (1 + df['Return']).cumprod() # 累積報酬（Cumulative Return）：將每日報酬連乘得到整段期間的資產成長曲線
    total_return = df['Cumulative'].iloc[-1] - 1 # 總報酬率（Total Return）：期末的累積報酬 - 1，就是整段投資期間的總報酬

    # 年化報酬率（CAGR）：將總報酬年化，使不同持有期間可以比較
    days = (df.index[-1] - df.index[0]).days
    cagr = (df['Cumulative'].iloc[-1]) ** (365 / days) - 1 if days > 0 else np.nan

    # 最大回撤（Max Drawdown）：表示從歷史最高點下跌的最大幅度。風險評估常用指標，用來衡量潛在損失有多大。
    roll_max = df['Cumulative'].cummax()
    drawdown = df['Cumulative'] / roll_max - 1
    max_drawdown = drawdown.min()

    # 夏普比率（Sharpe Ratio）：衡量單位風險所帶來的超額報酬。假設無風險利率為 0，可簡化為此公式。
    sharpe = np.sqrt(252) * df['Return'].mean() / df['Return'].std() if df['Return'].std() != 0 else np.nan

    return {
        "Total Return": total_return,
        "CAGR": cagr,
        "Max Drawdown": max_drawdown,
        "Sharpe Ratio": sharpe
    }


if __name__ == "__main__":
    input_dir = "output_historical_price_data"
    output_dir = "output_with_indicators"
    performance_dir = "output_backtesting_metrics"
    os.makedirs(output_dir, exist_ok=True) # 如果資料夾不存在就建立它
    os.makedirs(performance_dir, exist_ok=True)

    summary_path = os.path.join(performance_dir, "backtesting_performance_summary.csv") # 一行一檔 ETF，含 Total Return、CAGR、Max Drawdown、Sharpe
    summary_list = []

    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            ticker = file.replace(".csv", "")
            df = pd.read_csv(os.path.join(input_dir, file), index_col=0, parse_dates=True)

            if "Adj Close" in df.columns:
                df.rename(columns={"Adj Close": "Adj_Close"}, inplace=True)

            df = calculate_indicators(df)
            performance = evaluate_performance(df)
            performance["Ticker"] = ticker
            summary_list.append(performance)

            df.to_csv(os.path.join(output_dir, f"{ticker}_with_indicators.csv"))

    summary_df = pd.DataFrame(summary_list)
    summary_df = summary_df[["Ticker", "Total Return", "CAGR", "Max Drawdown", "Sharpe Ratio"]]
    summary_df.to_csv(summary_path, index=False)