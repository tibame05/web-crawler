import pandas as pd
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

if __name__ == "__main__":
    input_dir = "output_historical_price_data"
    output_dir = "output_with_indicators"
    os.makedirs(output_dir, exist_ok=True) # 如果資料夾不存在就建立它

    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            ticker = file.replace(".csv", "")
            df = pd.read_csv(os.path.join(input_dir, file), index_col=0, parse_dates=True)
            df = calculate_indicators(df)
            df.to_csv(os.path.join(output_dir, f"{ticker}_with_indicators.csv"))
