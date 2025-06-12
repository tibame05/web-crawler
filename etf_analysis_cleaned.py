# 載入套件
import mplfinance as mpf
import pandas as pd
import yfinance as yf
import os

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# 讀取上傳的 ETF CSV（預期包含 '序號' 欄位為 ticker）
etf_df = pd.read_csv("output/etf_list.csv", encoding="utf-8-sig", sep="\t")
etf_df.columns = etf_df.columns.str.strip()
ticker_list = etf_df["序號"].dropna().tolist()

# 下載各ETF從 2015-01-01 到今天的股價資料
for ticker in ticker_list:
    start_date = '2015-01-01'
    end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
    df = yf.download(ticker, start=start_date, end=end_date,multi_level_index = False, auto_adjust= False )
    df.to_csv(f"{output_dir}/{ticker}.csv")
